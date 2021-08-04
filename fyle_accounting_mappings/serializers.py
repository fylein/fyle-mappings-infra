"""
Mapping Serializers
"""
from rest_framework import serializers
from django.db.models.query import Q
from .models import ExpenseAttribute, DestinationAttribute, Mapping, MappingSetting, EmployeeMapping, CategoryMapping


class ExpenseAttributeSerializer(serializers.ModelSerializer):
    """
    Expense Attribute serializer
    """
    id = serializers.IntegerField()

    class Meta:
        model = ExpenseAttribute
        fields = '__all__'
        read_only_fields = (
            'value', 'attribute_type', 'source_id', 'workspace', 'detail',
            'auto_mapped', 'auto_created', 'active', 'display_name'
        )


class DestinationAttributeSerializer(serializers.ModelSerializer):
    """
    Destination Attribute serializer
    """
    id = serializers.IntegerField(allow_null=True)

    class Meta:
        model = DestinationAttribute
        fields = '__all__'
        read_only_fields = (
            'value', 'attribute_type', 'destination_id', 'workspace', 'detail',
            'auto_created', 'active', 'display_name'
        )


class MappingSettingSerializer(serializers.ModelSerializer):
    """
    Mapping Setting serializer
    """

    class Meta:
        model = MappingSetting
        fields = '__all__'


class MappingSerializer(serializers.ModelSerializer):
    """
    Mapping serializer
    """
    source = ExpenseAttributeSerializer()
    destination = DestinationAttributeSerializer()

    class Meta:
        model = Mapping
        fields = '__all__'


class EmployeeMappingSerializer(serializers.ModelSerializer):
    """
    Mapping serializer
    """
    source_employee = ExpenseAttributeSerializer(required=True)
    destination_employee = DestinationAttributeSerializer(allow_null=True)
    destination_vendor = DestinationAttributeSerializer(allow_null=True)
    destination_card_account = DestinationAttributeSerializer(allow_null=True)

    class Meta:
        model = EmployeeMapping
        fields = '__all__'

    def validate_source_employee(self, source_employee):
        attribute = ExpenseAttribute.objects.filter(
            id=source_employee['id'],
            workspace_id=self.initial_data['workspace'],
            attribute_type='EMPLOYEE'
        ).first()

        if not attribute:
            raise serializers.ValidationError('No attribute found with this attribute id')
        return source_employee

    def validate_destination_employee(self, destination_employee):
        if destination_employee and 'id' in destination_employee and destination_employee['id']:
            attribute = DestinationAttribute.objects.filter(
                id=destination_employee['id'],
                workspace_id=self.initial_data['workspace'],
                attribute_type='EMPLOYEE'
            ).first()

            if not attribute:
                raise serializers.ValidationError('No attribute found with this attribute id')
        return destination_employee

    def validate_destination_vendor(self, destination_vendor):
        if destination_vendor and 'id' in destination_vendor and destination_vendor['id']:
            attribute = DestinationAttribute.objects.filter(
                id=destination_vendor['id'],
                workspace_id=self.initial_data['workspace'],
                attribute_type='VENDOR'
            ).first()

            if not attribute:
                raise serializers.ValidationError('No attribute found with this attribute id')
        return destination_vendor

    def validate_destination_card_account(self, destination_card_account):
        if destination_card_account and 'id' in destination_card_account and destination_card_account['id']:
            attribute = DestinationAttribute.objects.filter(
                Q(attribute_type='CREDIT_CARD_ACCOUNT') | Q(attribute_type='CHARGE_CARD_NUMBER'),
                id=destination_card_account['id'],
                workspace_id=self.initial_data['workspace']
            ).first()

            if not attribute:
                raise serializers.ValidationError('No attribute found with this attribute id')
        return destination_card_account

    def create(self, validated_data):
        """
        Validated Data to be created
        :param validated_data:
        :return: Created Entry
        """
        employee_mapping = EmployeeMapping.create_or_update_employee_mapping(
            source_employee_id=validated_data['source_employee']['id'],
            workspace=validated_data['workspace'],
            destination_employee_id=validated_data['destination_employee']['id'],
            destination_vendor_id=validated_data['destination_vendor']['id'],
            destination_card_account_id=validated_data['destination_card_account']['id'],
            manual_mapping=True
        )

        return employee_mapping


class CategoryMappingSerializer(serializers.ModelSerializer):
    """
    Mapping serializer
    """
    source_category = ExpenseAttributeSerializer(required=True)
    destination_account = DestinationAttributeSerializer(allow_null=True)
    destination_expense_head = DestinationAttributeSerializer(allow_null=True)

    class Meta:
        model = CategoryMapping
        fields = '__all__'

    def validate_source_category(self, source_category):
        attribute = ExpenseAttribute.objects.filter(
            id=source_category['id'],
            workspace_id=self.initial_data['workspace'],
            attribute_type='CATEGORY'
        ).first()

        if not attribute:
            raise serializers.ValidationError('No attribute found with this attribute id')
        return source_category

    def validate_destination_account(self, destination_account):
        if destination_account and 'id' in destination_account and destination_account['id']:
            attribute = DestinationAttribute.objects.filter(
                id=destination_account['id'],
                workspace_id=self.initial_data['workspace'],
                attribute_type='ACCOUNT'
            ).first()

            if not attribute:
                raise serializers.ValidationError('No attribute found with this attribute id')
        return destination_account

    def validate_destination_expense_head(self, destination_expense_head):
        if destination_expense_head and 'id' in destination_expense_head and destination_expense_head['id']:
            attribute = DestinationAttribute.objects.filter(
                Q(attribute_type='EXPENSE_CATEGORY') | Q(attribute_type='EXPENSE_TYPE'),
                id=destination_expense_head['id'],
                workspace_id=self.initial_data['workspace']
            ).first()

            if not attribute:
                raise serializers.ValidationError('No attribute found with this attribute id')
        return destination_expense_head

    def create(self, validated_data):
        """
        Validated Data to be created
        :param validated_data:
        :return: Created Entry
        """
        category_mapping = CategoryMapping.create_or_update_category_mapping(
            source_category_id=validated_data['source_category']['id'],
            workspace=validated_data['workspace'],
            destination_expense_head_id=validated_data['destination_expense_head']['id'],
            destination_account_id=validated_data['destination_account']['id'],
            manual_mapping=True
        )

        return category_mapping
