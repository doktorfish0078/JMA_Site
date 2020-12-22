import unittest
from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import main
from main import Vacancy, CV


class SimpleTestCase(unittest.TestCase):
    global db
    db = SQLAlchemy(main.app)

    def test_deleting_ad(self):
        """Тест на проверку удаления объявления"""
        ad = main.Vacancy.query.first()  # берём самое первое объявление
        self.assertFalse(ad is None)  # убедимся,что оно есть
        id = ad.id
        main.delete_ad(id, 'my_vacancy')  # удалим его с помощь метода из main
        ad = main.Vacancy.query.get(id)  # попробуем снова взять его по индексу объявление
        self.assertTrue(ad is None)  # убедимся,что оно is None, тобишь не существует

    def test_create_ad(self):
        """ Не можем проверить сам метод create_vacancy или create_cv
        т.к. они работают только, получая POST метод, который невозможно смоделировать
        в модульных тестах,так что проверим просто саму логику доавбелния статьи в бд"""
        title = "Ищу красивую"
        description = "Именно её ищу"
        location = "Москва"
        price = "10000"
        vacancy = main.Vacancy(title=title, description=description, location=location, price=price)
        # Возьмём лист всех вакансий и узнаем его размер до добавления новой записи
        l = len(main.Vacancy.query.all())
        db.session.add(vacancy)
        db.session.commit()
        # Будем проверять, количество исходных записей + 1 и текущий размер листа с вакансиями.
        # Если они равны, то запись была добавлена
        self.assertEqual(l + 1, len(main.Vacancy.query.all()))

    def test_update_ad(self):
        """ Не можем проверить сам метод update_ad
            т.к. он работает только, получая POST метод, который невозможно смоделировать
            в модульных тестах,так что проверим не сам метод,а непосредственное
            изменение полей в статье бд"""
        test_vacancy = main.Vacancy.query.first()  # возьмём первую же вакансию
        self.assertNotEqual(test_vacancy.title, "Курьер")  # проверим,что на данный момент название вакансии не Курьер
        test_vacancy.title = "Курьер"  # сменим название на Курьер
        db.session.commit()  # закоммитим изменения в бд
        expected_vacancy = main.Vacancy.query.first()  # возьмём первую вакансию для проверка
        self.assertEqual(expected_vacancy.title, "Курьер")  # проверим изменилось ли название на Курьер

    def test_search_ad(self):
        """Проверка правильности поиска объявлений по названию"""
        text_search = 'aaa'  # текст поиска по названиям объявлений
        cv = main.CV.query.filter(text_search == CV.title).first()  # берём первое подходящее
        self.assertEqual(cv.title, text_search)  # проверяем,что нашли правильно

    def test_orderby_default_ad(self):
        """ Проверка корректности сортировки объявлений
        по умолчанию, тобишь от меньшего к большему значению id"""
        vacancies = Vacancy.query.order_by(Vacancy.id.asc()).all()  # сортирует объявления по возрастанию id
        last_id = -1
        for v in vacancies:
            self.assertTrue(v.id >= last_id)  # проверяем, чтобы каждый последующий встреченный id объявления был больше предыдущего
            last_id = v.id  # переприсваиваем id

    def test_orderby_title_ad(self):
        """ Проверка корректности сортировки объявлений
            по размеру названия от большему к меньшему"""
        vacancies = Vacancy.query.order_by(Vacancy.title.desc()).all()
        last_size_title = 70
        for v in vacancies:
            self.assertTrue(len(v.title) <= last_size_title)  # проверяем, чтобы длина названия каждого следующего элемента отсортированного списка объявлений была меньше предыдущей
            last_size_title = len(v.title)  # переприсваиваем длину названия объявления

    def test_orderby_price_desc_ad(self):
        """ Проверка корректности сортировки объявлений
            по цене от большего к меньшему значению"""
        vacancies = Vacancy.query.order_by(Vacancy.price.desc()).all()
        last_price = 10000000000
        for v in vacancies:
            self.assertTrue(int(v.price) <= last_price)
            last_price = v.price

    def test_orderby_price_asc_ad(self):
        """ Проверка корректности сортировки объявлений
            по цене от меньшего к большему значению"""
        vacancies = Vacancy.query.order_by(Vacancy.price.asc()).all()
        last_price = -10
        for v in vacancies:
            self.assertTrue(int(v.price) >= last_price)
            last_price = v.price

    def test_orderby_date_ad(self):
        """ Проверка корректности сортировки объявлений
            по дате от самого раннего до самого позднего"""
        last_date = datetime(2222, 1, 1)
        vacancies = Vacancy.query.order_by(Vacancy.date.desc()).all()
        for v in vacancies:
            self.assertTrue(v.date <= last_date)
            last_date = v.date
