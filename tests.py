import pytest
from main import BooksCollector


class TestBooksCollector:

    @pytest.fixture
    def collector(self):
        return BooksCollector()

    def test_add_new_book_valid_and_invalid(self, collector):
        """Тестирование добавления книг с валидными и невалидными названиями"""
        collector.add_new_book('Хроники Амбера')
        assert 'Хроники Амбера' in collector.books_genre
        assert collector.books_genre['Хроники Амбера'] == ''

        collector.add_new_book('Хроники Амбера')
        assert len(collector.books_genre) == 1

        collector.add_new_book('')
        collector.add_new_book('А' * 41)
        assert '' not in collector.books_genre
        assert 'А' * 41 not in collector.books_genre

    def test_set_book_genre_scenarios(self, collector):
        """Тестирование установки жанра в различных сценариях"""
        collector.add_new_book('Ложная слепота')
        collector.set_book_genre('Ложная слепота', 'Фантастика')
        assert collector.books_genre['Ложная слепота'] == 'Фантастика'

        collector.set_book_genre('Несуществующая книга', 'Фантастика')
        assert 'Несуществующая книга' not in collector.books_genre

        collector.add_new_book('Город и город')
        collector.set_book_genre('Город и город', 'Несуществующий жанр')
        assert collector.books_genre['Город и город'] == ''

    def test_get_book_genre_functionality(self, collector):
        """Тестирование получения жанра книги"""
        collector.add_new_book('Песнь льда и пламени')
        collector.add_new_book('Туманность Андромеды')

        collector.set_book_genre('Песнь льда и пламени', 'Фантастика')
        assert collector.get_book_genre('Песнь льда и пламени') == 'Фантастика'
        assert collector.get_book_genre('Туманность Андромеды') == ''
        assert collector.get_book_genre('Несуществующая') is None

    def test_get_books_with_specific_genre(self, collector):
        """Тестирование фильтрации книг по жанру"""
        collector.add_new_book('Ночной дозор')
        collector.add_new_book('Дневной дозор')
        collector.add_new_book('Убийство в Восточном экспрессе')

        collector.set_book_genre('Ночной дозор', 'Фантастика')
        collector.set_book_genre('Дневной дозор', 'Фантастика')
        collector.set_book_genre('Убийство в Восточном экспрессе', 'Детективы')

        fantasy_books = collector.get_books_with_specific_genre('Фантастика')
        assert len(fantasy_books) == 2
        assert 'Ночной дозор' in fantasy_books
        assert 'Дневной дозор' in fantasy_books

    def test_get_books_for_children_age_restriction(self, collector):
        """Тестирование фильтрации книг для детей"""
        collector.add_new_book('Винни-Пух')
        collector.add_new_book('Сияние')
        collector.add_new_book('Убийство по алфавиту')
        collector.add_new_book('Солярис')

        collector.set_book_genre('Винни-Пух', 'Мультфильмы')
        collector.set_book_genre('Сияние', 'Ужасы')
        collector.set_book_genre('Убийство по алфавиту', 'Детективы')
        collector.set_book_genre('Солярис', 'Фантастика')

        children_books = collector.get_books_for_children()
        assert 'Винни-Пух' in children_books
        assert 'Солярис' in children_books
        assert 'Сияние' not in children_books
        assert 'Убийство по алфавиту' not in children_books

    def test_add_to_favorites_functionality(self, collector):
        """Тестирование добавления книг в избранное"""
        collector.add_new_book('Американские боги')
        collector.add_new_book('Океан в конце дороги')

        collector.add_book_in_favorites('Американские боги')
        collector.add_book_in_favorites('Океан в конце дороги')
        collector.add_book_in_favorites('Американские боги')  # Дубликат
        collector.add_book_in_favorites('Несуществующая')  # Несуществующая

        assert len(collector.favorites) == 2
        assert 'Американские боги' in collector.favorites
        assert 'Океан в конце дороги' in collector.favorites

    def test_delete_from_favorites_functionality(self, collector):
        """Тестирование удаления книг из избранного"""
        collector.add_new_book('Задверье')
        collector.add_new_book('Сага о копье')

        collector.add_book_in_favorites('Задверье')
        collector.add_book_in_favorites('Сага о копье')

        collector.delete_book_from_favorites('Задверье')
        assert 'Задверье' not in collector.favorites
        assert 'Сага о копье' in collector.favorites

        collector.delete_book_from_favorites('Несуществующая')
        assert len(collector.favorites) == 1

    def test_get_list_of_favorites_books(self, collector):
        """Тестирование получения списка избранных книг"""
        collector.add_new_book('Хоббит')
        collector.add_new_book('Властелин колец')
        collector.add_new_book('Сильмариллион')

        collector.add_book_in_favorites('Хоббит')
        collector.add_book_in_favorites('Властелин колец')

        favorites = collector.get_list_of_favorites_books()
        assert len(favorites) == 2
        assert 'Хоббит' in favorites
        assert 'Властелин колец' in favorites
        assert 'Сильмариллион' not in favorites

    def test_get_books_genre_method(self, collector):
        """Тестирование получения всего словаря книг"""
        collector.add_new_book('Код да Винчи')
        collector.add_new_book('Ангелы и демоны')
        collector.set_book_genre('Код да Винчи', 'Детективы')

        books_genre = collector.get_books_genre()
        expected = {'Код да Винчи': 'Детективы', 'Ангелы и демоны': ''}
        assert books_genre == expected

    def test_initial_state_of_collector(self, collector):
        """Проверка начального состояния коллектора"""
        assert collector.books_genre == {}
        assert collector.favorites == []
        assert len(collector.genre) == 5
        assert len(collector.genre_age_rating) == 2

    def test_empty_favorites_list(self, collector):
        """Тестирование пустого списка избранного"""
        assert collector.get_list_of_favorites_books() == []

        collector.add_new_book('Книга')
        assert collector.get_list_of_favorites_books() == []

    def test_comprehensive_workflow(self, collector):
        """Комплексный тест полного workflow приложения"""
        books = ['Дракула', 'Франкенштейн', 'Кентервильское привидение']
        for book in books:
            collector.add_new_book(book)

        collector.set_book_genre('Дракула', 'Ужасы')
        collector.set_book_genre('Франкенштейн', 'Ужасы')
        collector.set_book_genre('Кентервильское привидение', 'Комедии')

        collector.add_book_in_favorites('Дракула')
        collector.add_book_in_favorites('Кентервильское привидение')

        assert collector.get_book_genre('Дракула') == 'Ужасы'
        assert len(collector.get_books_with_specific_genre('Ужасы')) == 2
        assert 'Кентервильское привидение' in collector.get_books_for_children()
        assert len(collector.get_list_of_favorites_books()) == 2