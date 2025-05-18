from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Admin, Candidat


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                'password', 'is_active', 'last_login')
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('id', 'last_login')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.is_active = True
        instance.save()
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class AdminTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        try:
            admin = Admin.objects.get(user=user)
            token = super().get_token(user)
            token['is_admin'] = True
            token['user_type'] = 'admin'
            return token
        except Admin.DoesNotExist:
            return None


class AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Admin
        fields = '__all__'
        read_only_fields = ['user']


class RegisterAdminSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Admin
        fields = ('username', 'email', 'password', 'password2',
                'first_name', 'last_name', 'telephone', 'role')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'telephone': {'required': True},
            'role': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Les mots de passe ne correspondent pas."})

        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError(
                {"email": "Un utilisateur avec cet email existe déjà."})

        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError(
                {"username": "Ce nom d'utilisateur est déjà pris."})

        return attrs

    def create(self, validated_data):
        password2 = validated_data.pop('password2')
        user_data = {
            'username': validated_data.pop('username'),
            'email': validated_data.pop('email'),
            'first_name': validated_data.pop('first_name'),
            'last_name': validated_data.pop('last_name'),
            'password': validated_data.pop('password')
        }

        user = User.objects.create_user(**user_data)
        user.is_staff = True
        user.save()

        admin = Admin.objects.create(user=user, **validated_data)
        return admin


class CandidatTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        try:
            candidat = Candidat.objects.get(user=user)
            token = super().get_token(user)
            token['is_admin'] = False
            token['user_type'] = 'candidat'
            return token
        except Candidat.DoesNotExist:
            return None


class CandidatSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Candidat
        fields = '__all__'
        read_only_fields = ['user']


class RegisterCandidatSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Candidat
        fields = ('username', 'email', 'password', 'password2',
                'first_name', 'last_name', 'date_naissance', 'telephone', 'adresse', 'cv')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'date_naissance': {'required': True},
            'telephone': {'required': True},
            'adresse': {'required': True},
            'cv': {'required': False}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Les mots de passe ne correspondent pas."})

        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError(
                {"email": "Un utilisateur avec cet email existe déjà."})

        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError(
                {"username": "Ce nom d'utilisateur est déjà pris."})

        return attrs

    def create(self, validated_data):
        password2 = validated_data.pop('password2')
        user_data = {
            'username': validated_data.pop('username'),
            'email': validated_data.pop('email'),
            'first_name': validated_data.pop('first_name'),
            'last_name': validated_data.pop('last_name'),
            'password': validated_data.pop('password')
        }

        user = User.objects.create_user(**user_data)
        user.save()

        candidat = Candidat.objects.create(user=user, **validated_data)
        return candidat


class UpdateCandidatProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    email = serializers.EmailField(source='user.email', required=False)

    class Meta:
        model = Candidat
        fields = ('first_name', 'last_name', 'email',
                'telephone', 'adresse', 'cv', 'date_naissance')
        read_only_fields = ['user']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user

        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance