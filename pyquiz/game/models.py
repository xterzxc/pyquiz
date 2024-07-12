from django.db import models


class Room(models.Model):
    active = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    host = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Player(models.Model):
    name = models.CharField(max_length=255)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} in {self.room.name}"

class Question(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    text = models.TextField()
    correct_code = models.TextField()
    time_limit = models.IntegerField()

    def __str__(self):
        return f"Question {self.id} in {self.room.name}"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    code = models.TextField()
    correct = models.BooleanField(default=False)
    submission_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer by {self.player.name} for question {self.question.id}"