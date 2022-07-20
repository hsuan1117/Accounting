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

## 交易類別 (TransactionCategory)

* id
* user_id
* title

## 物品類別 (ItemCategory)

* id
* title

## 交易 <-> 交易類別
`tablename` = `category_transaction`

| transaction_id | category_id |
| ----- | ----- |
| 1 | 2 |

# TODOs

* [X] Flask Migration: https://flask-migrate.readthedocs.io/en/latest/
* [] 設定帳本
* [] 修改帳目
* [] 物品增刪查改