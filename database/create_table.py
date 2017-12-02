create_blog_table = """
    create table blog(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title varchar(255) UNIQUE,
        file varchar(255),
        pic varchar(255),
        desc varchar(255),
        date REAL,
        cls varchar(255),
        FOREIGN KEY (cls) REFERENCES cls(name)
    );
"""
create_click_table ="""
    create table click(
        id INTEGER PRIMEAY KEY AUTOINCREMENT,
        blog_id INTEGER UNIQUE,
        number INTEGER,
        foreign key(blog_id) references blog(id)
    );
"""
create_comment_table = """
    create table comment(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        blog_id INTEGER,
        content varchar(255),
        foreign key (blog_id) references blog(id)
    )
"""
create_cls_table = """
    create table cls(
        id INTEGER PRIMARY KEY,
        name varchar(255) UNIQUE
    );
"""
