from django.db import models


# ======================================================================================================================
# ----- Application models
# ======================================================================================================================


class Host(models.Model):
    hosts = models.Manager()

    host_id = models.AutoField(db_column='VertskapID', primary_key=True)
    user_id = models.IntegerField(db_column='BrukerID')
    event_id = models.IntegerField(db_column='ArrangementID')

    class Meta:
        managed = False
        db_table = 'vertskap'


class User(models.Model):
    users = models.Manager()

    user_id = models.AutoField(db_column='BrukerID', primary_key=True)
    first_name = models.CharField(db_column='Fornavn', max_length=128)
    last_name = models.CharField(db_column='Etternavn', max_length=128)
    birth_date = models.DateTimeField(db_column='Fodselsdato', blank=True, null=True)
    address = models.CharField(db_column='Adresse', max_length=128, blank=True, null=True)
    post_code = models.IntegerField(db_column='Postnummer', blank=True, null=True)
    location = models.CharField(db_column='Sted', max_length=128, blank=True, null=True)
    is_admin = models.IntegerField(db_column='ErAdministrator')
    email = models.CharField(db_column='Epost', max_length=128)
    password = models.CharField(db_column='Passord', max_length=256)
    password_hash = models.CharField(db_column='PassordHash', max_length=256)

    class Meta:
        managed = False
        db_table = 'bruker'

    def display_name(self) -> str:
        return self.first_name + " " + self.last_name


class UserAllergy(models.Model):
    users_allergies = models.Manager()

    has_allergy_id = models.AutoField(db_column='HarallergiID', primary_key=True)
    user_id = models.IntegerField(db_column='BrukerID')
    ingredient_id = models.IntegerField(db_column='InnholdID')

    class Meta:
        managed = False
        db_table = 'harallergi'


class EventIngredient(models.Model):
    event_ingredients = models.Manager()

    event_ingredient_id = models.AutoField(db_column='ArrangementinnholdID', primary_key=True)
    event_id = models.IntegerField(db_column='ArrangementID')
    ingredient_id = models.IntegerField(db_column='InnholdID')

    class Meta:
        managed = False
        db_table = 'arrangementinnhold'


class Ingredient(models.Model):
    ingredients = models.Manager()

    ingredient_id = models.AutoField(db_column='InnholdID', primary_key=True)
    name = models.CharField(db_column='Navn', max_length=128)

    class Meta:
        managed = False
        db_table = 'innhold'


class Registration(models.Model):
    registrations = models.Manager()

    registration_id = models.AutoField(db_column='PaameldingID', primary_key=True)
    user_id = models.IntegerField(db_column='BrukerID')
    event_id = models.IntegerField(db_column='ArrangementID')
    # TODO: why does this have a date field? The date is available in the DinnerEvent model anyway.
    date = models.DateTimeField(db_column='Tidspunkt')

    class Meta:
        managed = False
        db_table = 'pamelding'


class DinnerEvent(models.Model):
    events = models.Manager()

    event_id = models.AutoField(db_column='ArrangementID', primary_key=True)
    name = models.CharField(db_column='ArrangementNavn', max_length=256)
    description = models.TextField(db_column='Beskrivelse', blank=True, null=True)
    capacity = models.IntegerField(db_column='AntallPlasser', blank=True, null=True)
    location = models.CharField(db_column='Lokasjon', max_length=128, blank=True, null=True)
    date = models.DateTimeField(db_column='Tidspunkt', blank=True, null=True)
    creation_date = models.DateTimeField(db_column='Opprettet')
    cost = models.IntegerField(db_column='Pris', blank=True, null=True)
    is_cancelled = models.IntegerField(db_column='Avlyst')

    class Meta:
        managed = False
        db_table = 'arrangement'

    def host(self) -> Host:
        return User.users.get(user_id=Host.hosts.get(event_id=self.event_id).user_id)

class Feedback(models.Model):
    feedbacks = models.Manager()

    feedbackid = models.AutoField(db_column='TilbakemeldingID', primary_key=True)  # Field name made lowercase.
    comment = models.CharField(db_column='Kommentar', max_length=500)  # Field name made lowercase.
    rating = models.IntegerField(db_column='Rating')  # Field name made lowercase.
    user_id_host = models.IntegerField(db_column='BrukerID_vertskap')  # Field name made lowercase.
    user_id_comment = models.IntegerField(db_column='BrukerID_kommentar')  # Field name made lowercase.
    event_id = models.IntegerField(db_column='ArrangementID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tilbakemelding'

# ======================================================================================================================
# ----- Authentication models
# ======================================================================================================================

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
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

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


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

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
