import asyncio
from decimal import Decimal

from sqlalchemy import select

from app.db.session import SessionLocal
from app.models import Categoria, Producto

CATEGORIES = [
    ('Casas de lujo', 'casas-de-lujo'),
    ('Departamentos', 'departamentos'),
    ('Propiedades comerciales', 'propiedades-comerciales'),
    ('Propiedades en alquiler', 'propiedades-en-alquiler'),
    ('Propiedades en preventa', 'propiedades-en-preventa'),
    ('Terrenos', 'terrenos'),
]

PROPERTIES = [
    ('Villa Redwood', 'Casa contemporánea con jardines privados y vistas abiertas al océano.', 'Malibu, California', 'PROP-REDWOOD-001', 'casas-de-lujo', 1850000, 8.75, 1, 'en_oferta'),
    ('Residencia Skyline', 'Residencia de autor con terraza panorámica y acabados de primera.', 'San Isidro, Lima', 'PROP-SKYLINE-002', 'casas-de-lujo', 920000, 9.20, 1, 'disponible'),
    ('Departamento Central Park', 'Departamento luminoso junto a parques, restaurantes y servicios.', 'Miraflores, Lima', 'PROP-CENTRAL-003', 'departamentos', 285000, 7.80, 2, 'disponible'),
    ('Casa Moderna Los Olivos', 'Vivienda funcional con patio, estacionamiento y gran proyección familiar.', 'Los Olivos, Lima', 'PROP-OLOIVOS-004', 'departamentos', 198000, 8.10, 1, 'disponible'),
    ('Torre Empresarial San Isidro', 'Oficina premium en edificio corporativo con alta demanda empresarial.', 'San Isidro, Lima', 'PROP-TORRE-005', 'propiedades-comerciales', 740000, 10.40, 3, 'en_oferta'),
    ('Terreno Campestre Cieneguilla', 'Lote amplio para proyecto residencial rodeado de naturaleza.', 'Cieneguilla, Lima', 'PROP-CIENE-006', 'terrenos', 165000, 11.00, 4, 'disponible'),
    ('Departamento Vista Mar', 'Hogar con balcón frente al mar y excelente potencial de alquiler temporal.', 'Barranco, Lima', 'PROP-VISTAMAR-007', 'propiedades-en-alquiler', 310000, 9.60, 1, 'alquilada'),
    ('Residencia Premium La Molina', 'Residencia espaciosa con seguridad, jardín y ambientes sociales.', 'La Molina, Lima', 'PROP-LAMOLINA-008', 'casas-de-lujo', 680000, 8.90, 1, 'reservada'),
    ('Parcela Valle Verde', 'Terreno de inversión con acceso a servicios y crecimiento urbano proyectado.', 'Lurín, Lima', 'PROP-VALLE-009', 'terrenos', 124000, 12.10, 6, 'disponible'),
    ('Locales Plaza Norte', 'Conjunto comercial con exposición a una zona de alto tránsito.', 'Independencia, Lima', 'PROP-PLAZA-010', 'propiedades-comerciales', 560000, 10.80, 2, 'disponible'),
]


async def seed() -> None:
    async with SessionLocal() as db:
        category_map: dict[str, Categoria] = {}
        categories_created = 0
        categories_existing = 0
        for name, slug in CATEGORIES:
            category = await db.scalar(select(Categoria).where(Categoria.slug == slug))
            if category is None:
                category = Categoria(nombre=name, slug=slug)
                db.add(category)
                categories_created += 1
            else:
                categories_existing += 1
            category_map[slug] = category
        await db.flush()

        properties_created = 0
        properties_existing = 0
        for name, description, location, sku, category_slug, price, yield_rate, stock, status in PROPERTIES:
            existing = await db.scalar(select(Producto).where(Producto.sku == sku))
            if existing is not None:
                properties_existing += 1
                continue
            db.add(Producto(
                categoria_id=category_map[category_slug].id,
                nombre=name,
                descripcion=description,
                ubicacion=location,
                sku=sku,
                precio=Decimal(str(price)),
                rentabilidad_estimada=Decimal(str(yield_rate)),
                stock=stock,
                imagen_url='/images/properties/property-placeholder.svg',
                estado=status,
                activo=True,
            ))
            properties_created += 1
        await db.commit()
    print(f'Categorias: {categories_created} creadas, {categories_existing} existentes')
    print(f'Propiedades: {properties_created} creadas, {properties_existing} existentes')


if __name__ == '__main__':
    asyncio.run(seed())
