# AirBnB clone - MySQL

Command interpreter plus two storage engines (JSON file and MySQL via
SQLAlchemy) behind the same code.

## Environment variables

| Variable | Meaning |
| --- | --- |
| HBNB_ENV | `dev` or `test` (`test` drops all tables at startup) |
| HBNB_MYSQL_USER / HBNB_MYSQL_PWD / HBNB_MYSQL_HOST / HBNB_MYSQL_DB | MySQL connection |
| HBNB_TYPE_STORAGE | `file` (default) or `db` |

## Setup

    cat setup_mysql_dev.sql | mysql -hlocalhost -uroot -p
    cat setup_mysql_test.sql | mysql -hlocalhost -uroot -p

## Usage

    echo 'create State name="California"' | ./console.py
    create Place city_id="1" user_id="2" name="My_house" number_rooms=4 latitude=37.77

## Tests

    python3 -m unittest discover tests
    HBNB_ENV=test HBNB_MYSQL_USER=hbnb_test HBNB_MYSQL_PWD=hbnb_test_pwd \
    HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_test_db \
    HBNB_TYPE_STORAGE=db python3 -m unittest discover tests

## Authors

- Initial authors of the AirBnB clone (keep the original names here)
- Add your name and your partner's name here
