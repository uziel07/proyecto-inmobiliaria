INSERT INTO productos (
    id,
    categoria_id,
    nombre,
    descripcion,
    ubicacion,
    sku,
    precio,
    rentabilidad_estimada,
    stock,
    imagen_url,
    estado,
    activo
)
SELECT
    uuid_generate_v4(),
    id,
    'Residencia Ocean View',
    'Propiedad moderna con vista panorámica y alto potencial de inversión.',
    'Asia, Lima',
    'PROP-OCEAN-001',
    480000.00,
    12.50,
    1,
    '/images/properties/property-placeholder.svg',
    'disponible',
    TRUE
FROM categorias
WHERE slug = 'casas-de-lujo'
  AND NOT EXISTS (SELECT 1 FROM productos WHERE sku = 'PROP-OCEAN-001')
LIMIT 1;
