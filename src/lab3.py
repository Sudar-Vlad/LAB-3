# ============================= УВАГА! =============================
# Цей файл містить ПРИКЛАД виконання лабораторної роботи.
# Ваше завдання - розробити ВЛАСНУ програму згідно з вашим варіантом.
#
# Ви можете використовувати цей код як зразок, але не копіювати його.
# Повністю замініть цей код своєю реалізацією.
#
# Ваш код повинен відповідати таким вимогам:
# 1. Обрана предметна область згідно з вашим варіантом.
# 2. Реалізовано всі необхідні функції:
#    - додавання, видалення, оновлення даних
#    - пошук та фільтрація
#    - обчислення статистик (середнє, min/max)
#    - групування та агрегація
# 3. Використано map(), filter(), reduce(), сортування, зрізи.
# 4. Реалізовано операції з множинами та словниками.
# 5. Створено інтерактивне меню для користувача.
# =================================================================

from collections import defaultdict
from functools import reduce
import datetime

# Початковий набір даних
music_collection = [
    {
        "artist": "Океан Ельзи",
        "country": "Україна",
        "albums": [
            {
                "title": "Модель",
                "year": 2001,
                "tracks": [
                    {"title": "911", "duration": 245, "genre": "Рок"},
                    {"title": "Модель", "duration": 270, "genre": "Рок"}
                ]
            }
        ]
    },
    {
        "artist": "The Weeknd",
        "country": "Канада",
        "albums": [
            {
                "title": "After Hours",
                "year": 2020,
                "tracks": [
                    {"title": "Blinding Lights", "duration": 200, "genre": "Поп"},
                    {"title": "Save Your Tears", "duration": 215, "genre": "Поп"}
                ]
            }
        ]
    },
    {
        "artist": "Queen",
        "country": "Велика Британія",
        "albums": [
            {
                "title": "A Night at the Opera",
                "year": 1975,
                "tracks": [
                    {"title": "Bohemian Rhapsody", "duration": 355, "genre": "Рок"},
                    {"title": "Love of My Life", "duration": 219, "genre": "Рок"}
                ]
            }
        ]
    }
]

# Допоміжні функції
def format_duration(seconds):
    """Перетворення секунд у формат хв:сек."""
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes}:{remaining_seconds:02d}"

def find_artist(artist_name):
    """Пошук виконавця за назвою."""
    return next(
        (
            artist for artist in music_collection
            if artist["artist"].lower() == artist_name.lower()
        ),
        None
    )

def find_album(album_title):
    """Пошук альбому в усій колекції."""
    for artist in music_collection:
        for album in artist["albums"]:
            if album["title"].lower() == album_title.lower():
                return artist, album
    return None, None

def get_all_tracks():
    """Отримання списку всіх треків."""
    return [
        {
            "artist": artist["artist"],
            "album": album["title"],
            "year": album["year"],
            **track
        }
        for artist in music_collection
        for album in artist["albums"]
        for track in album["tracks"]
    ]


# Додавання виконавця
def add_artist(name, country):
    if find_artist(name) is not None:
        print("Такий виконавець уже існує.")
        return

    music_collection.append({
        "artist": name,
        "country": country,
        "albums": []
    })
    print("Виконавця успішно додано.")


# Видалення виконавця
def delete_artist(name):
    artist = find_artist(name)

    if artist is None:
        print("Виконавця не знайдено.")
        return

    music_collection.remove(artist)
    print("Виконавця успішно видалено.")


# Оновлення інформації про виконавця
def update_artist(old_name, new_name, new_country):
    artist = find_artist(old_name)

    if artist is None:
        print("Виконавця не знайдено.")
        return

    artist["artist"] = new_name
    artist["country"] = new_country
    print("Дані виконавця оновлено.")

# Додавання альбому
def add_album(artist_name, album_title, year):
    artist = find_artist(artist_name)

    if artist is None:
        print("Виконавця не знайдено.")
        return

    if any(album["title"].lower() == album_title.lower()
           for album in artist["albums"]):
        print("Такий альбом уже існує.")
        return

    artist["albums"].append({
        "title": album_title,
        "year": year,
        "tracks": []
    })
    print("Альбом успішно додано.")

# Додавання треку
def add_track(artist_name, album_title, track_title, duration, genre):
    artist = find_artist(artist_name)

    if artist is None:
        print("Виконавця не знайдено.")
        return

    album = next(
        (
            album for album in artist["albums"]
            if album["title"].lower() == album_title.lower()
        ),
        None
    )

    if album is None:
        print("Альбом не знайдено.")
        return

    album["tracks"].append({
        "title": track_title,
        "duration": duration,
        "genre": genre
    })
    print("Трек успішно додано.")

# Пошук треків
def search_tracks(keyword):
    tracks = get_all_tracks()

    result = list(filter(
        lambda track:
        keyword.lower() in track["title"].lower()
        or keyword.lower() in track["artist"].lower()
        or keyword.lower() in track["album"].lower()
        or keyword.lower() in track["genre"].lower(),
        tracks
    ))

    if not result:
        print("Нічого не знайдено.")
        return

    for track in result:
        print(
            f'{track["artist"]} — {track["album"]} — '
            f'{track["title"]} ({format_duration(track["duration"])})'
        )

# Статистика колекції
def collection_statistics():
    tracks = get_all_tracks()

    if not tracks:
        print("Колекція порожня.")
        return

    durations = list(map(lambda track: track["duration"], tracks))

    total_duration = reduce(lambda x, y: x + y, durations, 0)
    average_duration = total_duration / len(durations)

    print(f"Кількість виконавців: {len(music_collection)}")
    print(f"Кількість альбомів: "
          f"{sum(len(artist['albums']) for artist in music_collection)}")
    print(f"Кількість треків: {len(tracks)}")
    print(f"Загальна тривалість: {format_duration(total_duration)}")
    print(f"Середня тривалість треку: "
          f"{format_duration(round(average_duration))}")
    print(f"Найкоротший трек: "
          f"{format_duration(min(durations))}")
    print(f"Найтриваліший трек: "
          f"{format_duration(max(durations))}")

# Групування треків за жанрами
def group_by_genre():
    genres = {}

    for track in get_all_tracks():
        genre = track["genre"]
        genres.setdefault(genre, []).append(track["title"])

    for genre, tracks in genres.items():
        print(f"\n{genre}:")
        for track in tracks:
            print(f"- {track}")

# Підрахунок кількості треків кожного виконавця
def artist_track_count():
    counts = {
        artist["artist"]: sum(
            len(album["tracks"]) for album in artist["albums"]
        )
        for artist in music_collection
    }

    for artist, count in counts.items():
        print(f"{artist}: {count} треків")

# Сортування треків за тривалістю
def sort_tracks_by_duration():
    tracks = sorted(
        get_all_tracks(),
        key=lambda track: track["duration"]
    )

    for track in tracks:
        print(
            f'{track["title"]} — '
            f'{format_duration(track["duration"])} — '
            f'{track["artist"]}'
        )

# Виведення колекції
def show_collection():
    for artist in music_collection:
        print(f"\nВиконавець: {artist['artist']}")
        print(f"Країна: {artist['country']}")

        for album in artist["albums"]:
            print(f"  Альбом: {album['title']} "
                  f"({album['year']})")

            for track in album["tracks"]:
                print(
                    f"    - {track['title']} "
                    f"({format_duration(track['duration'])}, "
                    f"{track['genre']})"
                )
# Інтерактивне меню
def menu():
    while True:
        print("""
== МУЗИЧНА КОЛЕКЦІЯ ==
1. Показати всю колекцію
2. Додати виконавця
3. Видалити виконавця
4. Оновити дані виконавця
5. Додати альбом
6. Додати трек
7. Пошук треків
8. Статистика колекції
9. Групування за жанрами
10. Кількість треків виконавців
11. Сортування треків за тривалістю
0. Вихід
""")

        choice = input("Оберіть пункт меню: ")

        if choice == "1":
            show_collection()

        elif choice == "2":
            name = input("Введіть ім'я виконавця: ")
            country = input("Введіть країну: ")
            add_artist(name, country)

        elif choice == "3":
            name = input("Введіть ім'я виконавця: ")
            delete_artist(name)

        elif choice == "4":
            old_name = input("Старе ім'я виконавця: ")
            new_name = input("Нове ім'я виконавця: ")
            country = input("Нова країна: ")
            update_artist(old_name, new_name, country)

        elif choice == "5":
            artist = input("Ім'я виконавця: ")
            title = input("Назва альбому: ")
            year = int(input("Рік випуску: "))
            add_album(artist, title, year)

        elif choice == "6":
            artist = input("Ім'я виконавця: ")
            album = input("Назва альбому: ")
            title = input("Назва треку: ")
            duration = int(input("Тривалість у секундах: "))
            genre = input("Жанр: ")
            add_track(artist, album, title, duration, genre)

        elif choice == "7":
            keyword = input("Введіть пошуковий запит: ")
            search_tracks(keyword)

        elif choice == "8":
            collection_statistics()

        elif choice == "9":
            group_by_genre()

        elif choice == "10":
            artist_track_count()

        elif choice == "11":
            sort_tracks_by_duration()

        elif choice == "0":
            print("Програму завершено.")
            breaK
        else:
            print("Неправильний пункт меню.")

if __name__ == "__main__":
    main()
