# 記帳軟體

# Models
## 帳本 (Book)
* user_id
* name

## 交易 (Transaction)
* id
* book_id
* name
* location
* items
* price
* created_at
* updated_at

## 物品 (Item)
* transaction_id
* name
* price

# TODOs
* [X] Flask Migration: https://flask-migrate.readthedocs.io/en/latest/