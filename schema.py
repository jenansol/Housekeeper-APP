# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AccountEmailaddress(models.Model):
    verified = models.BooleanField()
    primary = models.BooleanField()
    user = models.ForeignKey('AuthUser', models.DO_NOTHING)
    email = models.CharField(unique=True, max_length=254)

    class Meta:
        managed = False
        db_table = 'account_emailaddress'
        unique_together = (('user', 'primary'), ('user', 'email'),)


class AccountEmailconfirmation(models.Model):
    created = models.DateTimeField()
    sent = models.DateTimeField(blank=True, null=True)
    key = models.CharField(unique=True, max_length=64)
    email_address = models.ForeignKey(AccountEmailaddress, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_emailconfirmation'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DjangoSite(models.Model):
    name = models.CharField(max_length=50)
    domain = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'django_site'


class HousekeeperHirerequest(models.Model):
    requester_contact = models.CharField(max_length=100)
    request_date = models.DateField()
    requester = models.ForeignKey('LoginCustomuser', models.DO_NOTHING)
    housekeeper = models.ForeignKey('HousekeeperHousekeeper', models.DO_NOTHING)
    status = models.ForeignKey('HousekeeperStatus', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'housekeeper_hirerequest'


class HousekeeperHousekeeper(models.Model):
    name = models.CharField(db_column='Name', max_length=50)  # Field name made lowercase.
    age = models.IntegerField(db_column='Age')  # Field name made lowercase.
    nationality = models.ForeignKey('NationalityNationallity', models.DO_NOTHING)
    isactive = models.BooleanField()
    is_available = models.BooleanField()
    worked_before = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'housekeeper_housekeeper'


class HousekeeperRecruitmentrequest(models.Model):
    request_contact = models.CharField(max_length=100)
    requested_date = models.DateField()
    housekeeper = models.ForeignKey(HousekeeperHousekeeper, models.DO_NOTHING)
    requester = models.ForeignKey('LoginCustomuser', models.DO_NOTHING)
    visa_status = models.BooleanField()
    status = models.ForeignKey('HousekeeperStatus', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'housekeeper_recruitmentrequest'


class HousekeeperStatus(models.Model):
    status = models.CharField(db_column='Status', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'housekeeper_status'


class HousekeeperTransferrequest(models.Model):
    requested_date = models.DateField()
    housekeeper = models.ForeignKey(HousekeeperHousekeeper, models.DO_NOTHING)
    requester = models.ForeignKey('LoginCustomuser', models.DO_NOTHING)
    status = models.ForeignKey(HousekeeperStatus, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'housekeeper_transferrequest'


class LoginCustomuser(models.Model):
    last_login = models.DateTimeField(blank=True, null=True)
    password = models.CharField(max_length=128)
    phone_number = models.CharField(unique=True, max_length=17)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField()
    is_staff = models.BooleanField()
    fullname = models.CharField(db_column='fullName', unique=True, max_length=150)  # Field name made lowercase.
    dateofbirth = models.DateField(db_column='dateOfBirth')  # Field name made lowercase.
    nationalid = models.CharField(db_column='nationalID', max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'login_customuser'


class LoginProfile(models.Model):
    role = models.ForeignKey('RoleRole', models.DO_NOTHING, blank=True, null=True)
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'login_profile'


class NationalityNationallity(models.Model):
    nationality = models.CharField(db_column='Nationality', max_length=150)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'nationality_nationallity'


class PericePerNationalityPericepernationality(models.Model):
    price = models.FloatField()
    nationality = models.ForeignKey(NationalityNationallity, models.DO_NOTHING)
    service_type = models.ForeignKey('ServiceTypeServicetype', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'perice_per_nationality_pericepernationality'


class RoleRole(models.Model):
    name = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'role_role'


class ServiceTypeServicetype(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'service_type_servicetype'


class SocialaccountSocialaccount(models.Model):
    provider = models.CharField(max_length=200)
    uid = models.CharField(max_length=191)
    last_login = models.DateTimeField()
    date_joined = models.DateTimeField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    extra_data = models.JSONField()

    class Meta:
        managed = False
        db_table = 'socialaccount_socialaccount'
        unique_together = (('provider', 'uid'),)


class SocialaccountSocialapp(models.Model):
    provider = models.CharField(max_length=30)
    name = models.CharField(max_length=40)
    client_id = models.CharField(max_length=191)
    secret = models.CharField(max_length=191)
    key = models.CharField(max_length=191)
    provider_id = models.CharField(max_length=200)
    settings = models.JSONField()

    class Meta:
        managed = False
        db_table = 'socialaccount_socialapp'


class SocialaccountSocialappSites(models.Model):
    socialapp = models.ForeignKey(SocialaccountSocialapp, models.DO_NOTHING)
    site = models.ForeignKey(DjangoSite, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'socialaccount_socialapp_sites'
        unique_together = (('socialapp', 'site'),)


class SocialaccountSocialtoken(models.Model):
    token = models.TextField()
    token_secret = models.TextField()
    expires_at = models.DateTimeField(blank=True, null=True)
    account = models.ForeignKey(SocialaccountSocialaccount, models.DO_NOTHING)
    app = models.ForeignKey(SocialaccountSocialapp, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'socialaccount_socialtoken'
        unique_together = (('app', 'account'),)
