from sqlalchemy.inspection import inspect

def clean_sqlalchemy_object(obj):
    """Extract only column attributes from a SQLAlchemy object."""
    return {column.key: getattr(obj, column.key) for column in inspect(obj).mapper.column_attrs}

def paginate(items, page=1, per_page=10):
    total = len(items)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_items = items[start:end]

    response = {
        'items': [clean_sqlalchemy_object(item) for item in paginated_items],
        'total': total,
        'pages': (total / per_page if total % per_page == 0 else total // per_page + 1) ,
        'page': page,
    }

    return response
