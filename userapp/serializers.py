"""
Master:Chao
Datetime:2021/1/6 19:35
Reversion:1.0
File: serializers.py
"""
# 新建模型的序列化类，指明序列化的方式
from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # fields = "__all__"
        """
        此处若自定义序列化字段需要跟model模型类中字段保持一致
        否则引发Field name `info` is not valid for model `CustomUser`.错误
        """
        fields = ["username", "self_introduction", "headpic", "onlist", "email"]


class CustomUserRegistSerializers(serializers.ModelSerializer):
    password2 = serializers.CharField(label="重复密码", write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, attrs):
        password2 = attrs.pop("password2")
        password = attrs.get("password")
        if password2 != password:
            raise serializers.ValidationError("密码不一致")
        return attrs

    def create(self, validated_data):
        """
        创建用户
        :param validated_data:
        :return:用户
        """
        username = validated_data.__getitem__("username")
        email = validated_data.__getitem__("email")
        password = validated_data.__getitem__("password")
        user = CustomUser.objects.create_user(username=username, email=email, password=password)
        return user


class CustomUserHeadPicSerializers(serializers.ModelSerializer):
    headpic = serializers.ImageField()

    class Meta:
        model = CustomUser
        fields = ["headpic"]


class CustomUserPasswordSerializers(serializers.ModelSerializer):
    passwordold = serializers.CharField(write_only=True)
    passwordnew = serializers.CharField(write_only=True)
    passwordnew2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["passwordold", "passwordnew", "passwordnew2"]

    def validate(self, attrs):
        passwordold = attrs.get("passwordold")
        passwordnew = attrs.get("passwordnew")
        passwordnew2 = attrs.get("passwordnew2")
        user = self.context["request"].user
        if user.check_password(passwordold):
            if passwordnew == passwordnew2:
                return attrs
            else:
                raise serializers.ValidationError("密码不一致")
        else:
            raise serializers.ValidationError("原始密码错误")
