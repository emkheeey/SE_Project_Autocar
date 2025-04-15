-- Create profiles table
CREATE TABLE IF NOT EXISTS profiles (
    id BIGSERIAL PRIMARY KEY,
    user_id TEXT NOT NULL UNIQUE,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,
    
    -- Add these fields to match your Django model (if needed)
    phone_number TEXT,
    address TEXT
);

-- Create cars table
CREATE TABLE IF NOT EXISTS cars (
    id BIGSERIAL PRIMARY KEY,
    make TEXT NOT NULL,
    model TEXT NOT NULL,
    year INTEGER NOT NULL,
    price DECIMAL(10, 2),
    image_url TEXT,
    featured BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Set up Row Level Security (RLS) for profiles
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- Create policies for profiles table
CREATE POLICY "Public profiles are viewable by everyone"
    ON profiles FOR SELECT
    USING (true);

CREATE POLICY "Anyone can insert profiles"
    ON profiles FOR INSERT
    WITH CHECK (true);

CREATE POLICY "Users can update their own profile"
    ON profiles FOR UPDATE
    USING (true);

-- Set up Row Level Security (RLS) for cars
ALTER TABLE cars ENABLE ROW LEVEL SECURITY;

-- Create policies for cars table
CREATE POLICY "Cars are viewable by everyone"
    ON cars FOR SELECT
    USING (true);

CREATE POLICY "Only authenticated users can insert cars"
    ON cars FOR INSERT
    WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY "Only authenticated users can update cars"
    ON cars FOR UPDATE
    USING (auth.role() = 'authenticated');

-- Insert some sample cars
INSERT INTO cars (make, model, year, price, featured)
VALUES 
    ('Toyota', 'Camry', 2023, 25000.00, TRUE),
    ('Honda', 'Accord', 2022, 27000.00, TRUE),
    ('Ford', 'Mustang', 2023, 35000.00, TRUE),
    ('Chevrolet', 'Malibu', 2022, 23000.00, FALSE),
    ('Nissan', 'Altima', 2023, 24000.00, FALSE);

-- Add indexes for better query performance
CREATE INDEX idx_profiles_user_id ON profiles(user_id);
CREATE INDEX idx_cars_featured ON cars(featured); 