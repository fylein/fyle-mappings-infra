"""
Mapping Serializers
"""
from rest_framework import serializers
from .models import ExpenseAttribute, DestinationAttribute, Mapping, MappingSetting, EmployeeMapping


class ExpenseAttributeSerializer(serializers.ModelSerializer):
    """
    Expense Attribute serializer
    """
    id = serializers.IntegerField(write_only=True)

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
    id = serializers.IntegerField(write_only=True)

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
    destination_employee = DestinationAttributeSerializer()
    destination_vendor = DestinationAttributeSerializer()
    destination_card_account = DestinationAttributeSerializer()

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
            raise serializers.ValidationError("No attribute found with this attribute id")
        return source_employee

    def create(self, validated_data):
        """
        Validated Data to be created
        :param validated_data:
        :return: Created Entry
        """
        employee_mapping = EmployeeMapping.objects.update_or_create(
            source_employee=validated_data['source_employee']['id'],
            workspace=validated_data['workspace'],
            defaults={
                'destination_employee': validated_data['destination_employee']['id'],
                'destination_vendor': validated_data['destination_vendor']['id'],
                'destination_card_account': validated_data['destination_card_account']['id']
            }
        )

        return employee_mapping
