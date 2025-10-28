import os
import json

from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked



def on_reload():
    load_dotenv()
    os.makedirs('pages', exist_ok=True)
    file_path = os.getenv('FILE_PATH', 'meta_data.json')
    with open(file_path, 'r', encoding='utf8') as my_file:
        books = json.load(my_file)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    number_of_books = 10
    template = env.get_template('template.html')
    books_on_pages = list(chunked(books, number_of_books))
    for number, books_on_page in enumerate(books_on_pages):        
        rendered_page = template.render(
        books = books_on_page,
        current_page = number + 1,  
        total_pages = len(books_on_pages)
        )
        with open(f'pages/index{number + 1}.html', 'w', encoding='utf8') as file:
            file.write(rendered_page)


def main():
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.', default_filename='./pages/index1.html')
    


if __name__ == '__main__':
    main()