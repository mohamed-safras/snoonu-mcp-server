CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE TABLE categories (
  id    SERIAL PRIMARY KEY,
  name  TEXT NOT NULL,
  slug  TEXT NOT NULL UNIQUE
);

CREATE TABLE products (
  id                TEXT PRIMARY KEY,
  name              TEXT NOT NULL,
  summary           TEXT,
  description       TEXT,
  category_id       INT REFERENCES categories(id),
  price_amount      NUMERIC(10,2) NOT NULL,
  price_currency    TEXT NOT NULL DEFAULT 'QAR',
  compare_at_amount NUMERIC(10,2),
  in_stock          BOOLEAN NOT NULL DEFAULT TRUE,
  stock_level       TEXT,
  image_url         TEXT,
  images            TEXT[],
  rating            NUMERIC(2,1),
  url               TEXT,
  created_at        TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX products_name_trgm_idx ON products USING gin (name gin_trgm_ops);
CREATE INDEX products_category_idx ON products (category_id);

CREATE TABLE cities (
  id      SERIAL PRIMARY KEY,
  name    TEXT NOT NULL,
  lat     NUMERIC(9,6) NOT NULL,
  lng     NUMERIC(9,6) NOT NULL,
  aliases TEXT[]
);

CREATE TABLE orders (
  id            TEXT PRIMARY KEY,
  status        TEXT NOT NULL DEFAULT 'pending_payment',
  total_amount  NUMERIC(10,2) NOT NULL,
  currency      TEXT NOT NULL DEFAULT 'QAR',
  recipient     JSONB NOT NULL,
  delivery      JSONB NOT NULL,
  sender        JSONB NOT NULL,
  gift_message  TEXT,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
  expires_at    TIMESTAMPTZ
);

CREATE TABLE order_items (
  id          SERIAL PRIMARY KEY,
  order_id    TEXT REFERENCES orders(id) ON DELETE CASCADE,
  product_id  TEXT REFERENCES products(id),
  quantity    INT NOT NULL,
  icing_text  TEXT
);
