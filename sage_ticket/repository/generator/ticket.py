import functools
import os
import random
from typing import Any, List

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from mimesis import Person, Text
from mimesis.locales import Locale
from tqdm import tqdm

from sage_ticket.helper import ExtensionsEnum, SeverityEnum, StatusEnum, TicketStateEnum
from sage_ticket.models import Attachment, Comment, Department, Issue

User = get_user_model()


class TicketDataGenerator:
    def __init__(self):
        self.person = Person(Locale.EN)
        self.text = Text(Locale.EN)

    def create_users(self, total):
        objs = [
            User(
                username=f"{self.person.username()}{i}",
                email=self.person.email(domains=["sageteam.org", "radin.com"]),
                password=self.person.password(length=12, hashed=True),
            )
            for i in tqdm(range(total))
        ]
        users = User.objects.bulk_create(objs, batch_size=1000)
        return users

    def create_department(self, total):
        objs = [
            Department(
                description=self.text.text(quantity=5),
                title=self.text.title(),
            )
            for _ in range(total)
        ]
        departments = Department.objects.bulk_create(objs)
        return departments

    def create_comment(self, total, users, issues):
        objs = [
            Comment(
                user=random.choice(users),
                issue=random.choice(issues),
                message=self.text.text(quantity=3),
                title=self.text.title(),
                status=random.choice(StatusEnum.choices)[0],
                is_read=True,
            )
            for i in tqdm(range(total))
        ]
        comments = Comment.objects.bulk_create(objs)
        return comments

    def create_issue(self, total, users, departments):
        objs = [
            Issue(
                raised_by=random.choice(users),
                message=self.text.text(quantity=3),
                department=random.choice(departments),
                subject=self.text.title(),
                state=random.choice(TicketStateEnum.choices)[0],
                severity=random.choice(SeverityEnum.choices)[0],
            )
            for i in tqdm(range(total))
        ]
        issues = Issue.objects.bulk_create(objs)
        return issues

    def create_attachment(self, total, issues):
        files = self.get_random_f()
        objs = [
            Attachment(
                issue=random.choice(issues),
                name=self.text.text(quantity=1),
                file=SimpleUploadedFile(
                    name=random.choice(files)[0], content=random.choice(files)[1]
                ),
                extensions=random.choice(ExtensionsEnum.choices)[0],
            )
            for i in tqdm(range(total))
        ]
        attachments = Attachment.objects.bulk_create(objs)
        return attachments

    def get_random_f(self):
        demo_pic_dir_path = os.path.join(
            settings.BASE_DIR,
            "media",
            "demo",
        )
        files = []

        for root, dirs, files in os.walk(demo_pic_dir_path, topdown=False):
            for name in files:
                pic_path = os.path.join(root, name)
                with open(pic_path, mode="rb") as demo_pic:
                    picture = demo_pic.read()
                data = (pic_path, picture)
                files.append(data)
        return files

    def add_2_m_m(self, objs: List[Any], target_field: str, item_per_obj: int, item):
        attr = getattr(item, target_field)
        try:
            items_to_add = list(map(lambda _: random.choice(objs), range(item_per_obj)))
        except IndexError as exc:
            print(exc)
            raise IndexError("objs are empty")

        attr.add(*items_to_add)

    def join_members(self, departments, members, total):
        joiner = functools.partial(self.add_2_m_m, members, "member", total)
        result = list(tqdm(map(joiner, departments)))
        print(result)
        return departments
