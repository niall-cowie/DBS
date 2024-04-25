from django.db import models

class Person(models.Model):
    member_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.IntegerField()
    class Meta:
        indexes = [
            models.Index(fields=['age'])  #index on the age field to speed up filtering by age
        ]
    def __str__(self):
        return self.member_id + self.first_name + ' ' + self.last_name

class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=30)
    course_par = models.IntegerField()

    class Meta:
        indexes = [
            models.Index(fields=['course_par'])
        ]

class Tee_Time(models.Model):
    tee_time_id = models.AutoField(primary_key=True)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    group_size = models.IntegerField()
    tee_date_time = models.DateTimeField()

class Tee_Time_Group_Member(models.Model):
    tee_time = models.ForeignKey(Tee_Time, on_delete=models.CASCADE)
    participant = models.ForeignKey(Person, on_delete=models.CASCADE)
