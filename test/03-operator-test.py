
import user_docs


def setup():
    user_docs.create_db_and_indexes()


def test_all():
    db = user_docs.mkdb()
    docs = db.find({
            "manager": True,
            "favorites": {"$all": ["Lisp", "Python"]}
        })
    assert len(docs) == 3
    assert docs[0]["user_id"] == 2
    assert docs[1]["user_id"] == 12
    assert docs[2]["user_id"] == 9


def test_all_non_array():
    db = user_docs.mkdb()
    docs = db.find({
            "manager": True,
            "location": {"$all": ["Ohai"]}
        })
    assert len(docs) == 0


def test_elem_match():
    db = user_docs.mkdb()
    emdocs = [
        {
            "user_id": "a",
            "bang": [{
                "foo": 1,
                "bar": 2
            }]
        },
        {
            "user_id": "b",
            "bang": [{
                "foo": 2,
                "bam": True
            }]
        }
    ]
    db.save_docs(emdocs)
    docs = db.find({
        "_id": {"$gt": None},
        "bang": {"$elemMatch": {
            "foo": {"$gte": 1},
            "bam": True
        }}
    })
    assert len(docs) == 1
    assert docs[0]["user_id"] == "b"


def test_regex():
    db = user_docs.mkdb()

    docs = db.find({
            "age": {"$gt": 40},
            "location.state": {"$regex": "(?i)new.*"}
        })
    assert len(docs) == 2
    assert docs[0]["user_id"] == 2
    assert docs[1]["user_id"] == 10


def test_in_operator_array():
    db = user_docs.mkdb()

    docs = db.find({
            "manager": True,
            "favorites": {"$in": ["Ruby", "Python"]}
        })
    assert len(docs) == 7
    assert docs[0]["user_id"] == 2
    assert docs[1]["user_id"] == 12
