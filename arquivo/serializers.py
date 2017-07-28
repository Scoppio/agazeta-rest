import uuid
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import serializers
from .models import Profile, TobToken


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # A field from the user's profile:
    avatar = serializers.SerializerMethodField(read_only=True)
    partner_sub = serializers.BooleanField(source='profile.partner_sub')
    account_type = serializers.CharField(source='profile.account_type', max_length=80, write_only=True, allow_blank=True)
    newsletter_sub = serializers.BooleanField(source='profile.newsletter_sub')
    #key = serializers.CharField(max_length=80, write_only=True, allow_blank=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'first_name', 'last_name', 'password', 'email', 'avatar', 'account_type', 'partner_sub', 'newsletter_sub')

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        user = super(UserSerializer, self).create(validated_data)
        self.update_or_create_profile(user, profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        self.update_or_create_profile(instance, profile_data)
        return super(UserSerializer, self).update(instance, validated_data)

    def update_or_create_profile(self, user, profile_data):
        # This always creates a Profile if the User is missing one;
        # change the logic here if that's not right for your app
        Profile.objects.update_or_create(user=user, defaults=profile_data)

    def get_avatar(self, obj):
        avatar = reverse('django_pydenticon:image',  kwargs={"data": uuid.uuid3(uuid.NAMESPACE_X500, obj.email+obj.username)});
        return avatar


class TobTokenSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = TobToken
        fields = ('username', 'token', 'server', 'is_active', 'user')


class TobTokenSerializerVersion1(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TobToken
        fields = ('username', 'token', 'is_active')

#
# class MCardSerializer(mSerializers.DocumentSerializer):
#     card = StringField(max_length=30)
#     turn_played = IntField()
#     is_spawned = BooleanField()
#
#
# class MMatchSerializer(mSerializers.DocumentSerializer):
#     match_id = IntField()
#     match_mode = StringField(max_length=30)
#     user = ListField(child=serializers.IntegerField())
#     date = DateTimeField()
#     blue_rank = IntField()
#     blue_hero = StringField(max_length=30)
#     blue_deck = StringField(max_length=30)
#     red_hero = StringField(max_length=30)
#     red_deck = StringField(max_length=30)
#     turns_played = IntField()
#     red_starts = BooleanField()
#     blue_won = BooleanField()
#     blue_played_cards =ListField(ReferenceField(MCardPlayed))
#     red_played_cards = ListField(ReferenceField(MCardPlayed))