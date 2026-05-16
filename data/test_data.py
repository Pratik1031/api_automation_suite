from faker import Faker

fake = Faker()


def valid_post_payload(user_id: int = 1) -> dict:
    return {
        "userId": user_id,
        "title": fake.sentence(nb_words=6).rstrip("."),
        "body": fake.paragraph(nb_sentences=3),
    }


def valid_user_payload() -> dict:
    username = fake.user_name()
    return {
        "name": fake.name(),
        "username": username,
        "email": fake.email(),
        "phone": fake.phone_number(),
        "website": fake.domain_name(),
    }


BOUNDARY_TITLES = {
    "single_char": "A",
    "exactly_255": "B" * 255,
    "exceeds_255": "C" * 256,
    "empty": "",
    "whitespace_only": "   ",
    "special_chars": "!@#$%^&*()<>?/|}{~:",
    "unicode": "日本語タイトル テスト",
    "sql_injection": "' OR '1'='1",
    "html_injection": "<script>alert('xss')</script>",
    "numeric_string": "12345",
}

INVALID_USER_IDS = [-1, 0, 9999999, "abc", None, "", "!@#"]

VALID_USER_IDS = [1, 2, 5, 10]
