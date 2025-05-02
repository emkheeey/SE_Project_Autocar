-- Drop existing tables and constraints if they exist
DROP TABLE IF EXISTS cars CASCADE;
DROP TABLE IF EXISTS profiles CASCADE;

-- Create profiles table
CREATE TABLE IF NOT EXISTS profiles (
    id BIGSERIAL PRIMARY KEY,
    user_id TEXT NOT NULL UNIQUE,
    username TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,
    
    -- Add these fields to match your Django model (if needed)
    phone_number TEXT,
    address TEXT
);

-- Create cars table with detailed Toyota specifications
CREATE TABLE IF NOT EXISTS cars (
    id BIGSERIAL PRIMARY KEY,
    model TEXT NOT NULL,
    year INTEGER NOT NULL,
    price DECIMAL(10, 2),
    image_url TEXT,
    featured BOOLEAN DEFAULT FALSE,
    body_type TEXT NOT NULL CHECK (body_type IN ('Sedan', 'SUV', 'MPV', 'Minivan', 'Hatchback', 'Pickup', 'Van', 'Coupe')),
    transmission TEXT NOT NULL CHECK (transmission IN ('Automatic', 'CVT', 'Manual')),
    fuel_type TEXT NOT NULL CHECK (fuel_type IN ('Petrol', 'Diesel', 'Hybrid', 'Electric')),
    num_seats INTEGER NOT NULL CHECK (num_seats BETWEEN 2 AND 30),  -- Updated to allow more seats
    max_output TEXT NOT NULL,  -- Format: "247 hp @ 6,000 rpm"
    drivetrain TEXT NOT NULL CHECK (drivetrain IN ('Front-Wheel Drive', 'Rear-Wheel Drive', 'All-Wheel Drive')),
    wheel_size TEXT NOT NULL,  -- Format: "19 in"
    airbags INTEGER NOT NULL CHECK (airbags BETWEEN 2 AND 10),
    isofix BOOLEAN NOT NULL,
    front_parking_sensors BOOLEAN NOT NULL,
    rear_parking_sensors BOOLEAN NOT NULL,
    connectivity TEXT[] NOT NULL,  -- Array of available connectivity features
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

-- Add indexes for better query performance
CREATE INDEX idx_profiles_user_id ON profiles(user_id);
CREATE INDEX idx_cars_featured ON cars(featured);
CREATE INDEX idx_cars_model ON cars(model);
CREATE INDEX idx_cars_body_type ON cars(body_type);
CREATE INDEX idx_cars_fuel_type ON cars(fuel_type);
CREATE INDEX idx_cars_price ON cars(price);

-- Insert all Toyota models available in the Philippines
INSERT INTO cars (
    model, year, price, featured, body_type, transmission, fuel_type, 
    num_seats, max_output, drivetrain, wheel_size, airbags, isofix,
    front_parking_sensors, rear_parking_sensors, connectivity
)
VALUES 
    -- Sedans
    ('Camry', 2024, 2657000.00, TRUE, 'Sedan', 'CVT', 'Hybrid',
     5, '215 hp @ 5,700 rpm', 'Front-Wheel Drive', '18 in', 7, TRUE,
     TRUE, TRUE, ARRAY['AM', 'FM', 'Bluetooth', 'Apple CarPlay', 'Android Auto', 'Voice Comm']),
     
    ('Corolla Altis', 2024, 1213000.00, TRUE, 'Sedan', 'CVT', 'Hybrid',
     5, '121 hp @ 6,000 rpm', 'Front-Wheel Drive', '16 in', 7, TRUE,
     TRUE, TRUE, ARRAY['AM', 'FM', 'Bluetooth', 'Apple CarPlay', 'Android Auto', 'Voice Comm']),
     
    ('Vios', 2024, 738000.00, TRUE, 'Sedan', 'CVT', 'Petrol',
     5, '98 hp @ 6,000 rpm', 'Front-Wheel Drive', '15 in', 7, TRUE,
     TRUE, TRUE, ARRAY['AM', 'FM', 'Bluetooth', 'Apple CarPlay', 'Android Auto']),
     
    -- SUVs
    ('Corolla Cross', 2024, 1514000.00, TRUE, 'SUV', 'CVT', 'Hybrid',
     5, '196 hp @ 6,000 rpm', 'Front-Wheel Drive', '18 in', 7, TRUE,
     TRUE, TRUE, ARRAY['AM', 'FM', 'Bluetooth', 'Apple CarPlay', 'Android Auto', 'Voice Comm']),
     
    ('Fortuner', 2024, 1775000.00, TRUE, 'SUV', 'Automatic', 'Diesel',
     7, '201 hp @ 3,400 rpm', 'Rear-Wheel Drive', '17 in', 7, TRUE,
     TRUE, TRUE, ARRAY['AM', 'FM', 'Bluetooth', 'Apple CarPlay', 'Android Auto', 'Voice Comm']),
     
    ('RAV4', 2024, 2052000.00, TRUE, 'SUV', 'CVT', 'Hybrid',
     5, '219 hp @ 5,700 rpm', 'All-Wheel Drive', '18 in', 7, TRUE,
     TRUE, TRUE, ARRAY['AM', 'FM', 'Bluetooth', 'Apple CarPlay', 'Android Auto', 'Voice Comm']),
     
    ('Rush', 2024, 1208000.00, TRUE, 'SUV', 'Automatic', 'Petrol',
     7, '102 hp @ 6,000 rpm', 'Rear-Wheel Drive', '16 in', 7, TRUE,
     TRUE, TRUE, ARRAY['AM', 'FM', 'Bluetooth', 'Apple CarPlay', 'Android Auto']),
     
    ('Yaris Cross', 2024, 1210000.00, TRUE, 'SUV', 'CVT', 'Hybrid',
     5, '91 hp @ 5,500 rpm', 'Front-Wheel Drive', '17 in', 7, TRUE,
     TRUE, TRUE, ARRAY['AM', 'FM', 'Bluetooth', 'Apple CarPlay', 'Android Auto']),
     
    -- MPVs and Minivans
    ('Alphard', 2024, 4671000.00, TRUE, 'Minivan', 'CVT', 'Hybrid',
     7, '247 hp @ 6,000 rpm', 'Front-Wheel Drive', '19 in', 6, TRUE,
     TRUE, TRUE, ARRAY['AM', 'FM', 'Bluetooth', 'Apple CarPlay', 'Android Auto', 'Voice Comm']),
     
    ('Avanza', 2024, 844000.00, TRUE, 'MPV', 'CVT', 'Petrol',
     7, '105 hp @ 6,000 rpm', 'Front-Wheel Drive', '15 in', 7, TRUE,
     TRUE, TRUE, ARRAY['AM', 'FM', 'Bluetooth', 'Apple CarPlay', 'Android Auto']),
     
    ('Innova', 2024, 1267000.00, TRUE, 'MPV', 'Automatic', 'Diesel',
     7, '148 hp @ 3,400 rpm', 'Rear-Wheel Drive', '16 in', 7, TRUE,
     TRUE, TRUE, ARRAY['AM', 'FM', 'Bluetooth', 'Apple CarPlay', 'Android Auto']),
     
    ('Veloz', 2024, 1104000.00, TRUE, 'MPV', 'CVT', 'Petrol',
     7, '105 hp @ 6,000 rpm', 'Front-Wheel Drive', '16 in', 7, TRUE,
     TRUE, TRUE, ARRAY['AM', 'FM', 'Bluetooth', 'Apple CarPlay', 'Android Auto']),
     
    ('Zenix', 2024, 1676000.00, TRUE, 'MPV', 'CVT', 'Hybrid',
     7, '186 hp @ 6,000 rpm', 'Front-Wheel Drive', '17 in', 7, TRUE,
     TRUE, TRUE, ARRAY['AM', 'FM', 'Bluetooth', 'Apple CarPlay', 'Android Auto', 'Voice Comm']),
     
    -- Pickups
    ('Hilux', 2024, 891000.00, TRUE, 'Pickup', 'Automatic', 'Diesel',
     5, '201 hp @ 3,400 rpm', 'Rear-Wheel Drive', '17 in', 7, TRUE,
     TRUE, TRUE, ARRAY['AM', 'FM', 'Bluetooth', 'Apple CarPlay', 'Android Auto']),
     
    -- Vans
    ('Hiace', 2024, 1195000.00, TRUE, 'Van', 'Automatic', 'Diesel',
     15, '134 hp @ 3,400 rpm', 'Rear-Wheel Drive', '16 in', 7, TRUE,
     TRUE, TRUE, ARRAY['AM', 'FM', 'Bluetooth', 'Apple CarPlay', 'Android Auto']),
     
    ('Hiace Super Grandia', 2024, 2906000.00, TRUE, 'Van', 'Automatic', 'Diesel',
     12, '134 hp @ 3,400 rpm', 'Rear-Wheel Drive', '16 in', 7, TRUE,
     TRUE, TRUE, ARRAY['AM', 'FM', 'Bluetooth', 'Apple CarPlay', 'Android Auto', 'Voice Comm']),
     
    ('Coaster', 2024, 4114000.00, TRUE, 'Van', 'Automatic', 'Diesel',
     29, '134 hp @ 3,400 rpm', 'Rear-Wheel Drive', '16 in', 7, TRUE,
     TRUE, TRUE, ARRAY['AM', 'FM', 'Bluetooth', 'Apple CarPlay', 'Android Auto']),
     
    -- Hatchbacks
    ('Wigo', 2024, 615000.00, TRUE, 'Hatchback', 'CVT', 'Petrol',
     5, '88 hp @ 6,000 rpm', 'Front-Wheel Drive', '14 in', 7, TRUE,
     TRUE, TRUE, ARRAY['AM', 'FM', 'Bluetooth', 'Apple CarPlay', 'Android Auto']),
     
    -- Performance Cars
    ('GR Supra', 2024, 5552000.00, TRUE, 'Coupe', 'Automatic', 'Petrol',
     2, '382 hp @ 5,800 rpm', 'Rear-Wheel Drive', '19 in', 7, TRUE,
     TRUE, TRUE, ARRAY['AM', 'FM', 'Bluetooth', 'Apple CarPlay', 'Android Auto', 'Voice Comm']),
     
    ('GR Yaris', 2024, 3391000.00, TRUE, 'Hatchback', 'Manual', 'Petrol',
     4, '257 hp @ 6,500 rpm', 'All-Wheel Drive', '18 in', 7, TRUE,
     TRUE, TRUE, ARRAY['AM', 'FM', 'Bluetooth', 'Apple CarPlay', 'Android Auto', 'Voice Comm']),
     
    ('GR86', 2024, 2716000.00, TRUE, 'Coupe', 'Manual', 'Petrol',
     2, '228 hp @ 7,000 rpm', 'Rear-Wheel Drive', '18 in', 7, TRUE,
     TRUE, TRUE, ARRAY['AM', 'FM', 'Bluetooth', 'Apple CarPlay', 'Android Auto', 'Voice Comm']); 