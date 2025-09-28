<<<<<<< HEAD
from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
=======
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
>>>>>>> 1ecd32d1dea72500a859144e08de7e420a893bd4


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
<<<<<<< HEAD
        fields = ['id', 'username', 'password',
                  'email', 'first_name', 'last_name']


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 
=======
        fields = ['id', 'username', 'password', 'email',
>>>>>>> 1ecd32d1dea72500a859144e08de7e420a893bd4
                  'first_name', 'last_name']
