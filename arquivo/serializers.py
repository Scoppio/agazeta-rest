import uuid
import json
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import serializers
from .models import Profile, TobToken
from .documents import MMatch


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


class MCardSerializer(serializers.Serializer):
    card = serializers.CharField(max_length=30)
    turn_played = serializers.IntegerField()
    is_spawned = serializers.BooleanField()


class MMatchSerializer(serializers.Serializer):
    match_id =  serializers.IntegerField()
    match_mode = serializers.CharField(max_length=30)
    # the user should not appear unless
    user = serializers.ReadOnlyField(source='user.id')
    date = serializers.DateTimeField()
    blue_rank =  serializers.IntegerField()
    blue_hero = serializers.CharField(max_length=30)
    blue_deck = serializers.CharField(max_length=30)
    red_hero = serializers.CharField(max_length=30)
    red_deck = serializers.CharField(max_length=30)
    turns_played =  serializers.IntegerField()
    red_starts = serializers.BooleanField()
    blue_won = serializers.BooleanField()
    blue_played_cards = serializers.SerializerMethodField()
    red_played_cards = serializers.SerializerMethodField()

    def get_blue_played_cards(self, obj):
        return [card.__dict__() for card in obj.red_played_cards]

    def get_red_played_cards(self, obj):
        return [card.__dict__() for card in obj.red_played_cards]