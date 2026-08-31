"""
E-Commerce Rich Catalog & Order Data
Comprehensive inventory of in-stock items across multiple popular categories.
"""

CATALOG_PRODUCTS = [
    # --- ELECTRONICS & AUDIO ---
    {
        "id": 1,
        "name": "NovaPulse Pro Wireless Noise-Cancelling Headphones",
        "category": "Electronics & Audio",
        "price": 8999.0,
        "stock": 45,
        "rating": 4.8,
        "description": "Premium active noise cancelling over-ear Bluetooth headphones with 40-hour battery life, deep bass, spatial audio, and ultra-comfortable memory foam ear cushions."
    },
    {
        "id": 2,
        "name": "AirSound Pods Pro True Wireless Earbuds",
        "category": "Electronics & Audio",
        "price": 4500.0,
        "stock": 70,
        "rating": 4.7,
        "description": "Crystal clear wireless earbuds with ENC dual microphone for HD calls, IPX5 sweat resistance, touch controls, and compact USB-C fast charging case."
    },
    {
        "id": 3,
        "name": "HyperBeam 4K Ultra HD Gaming Monitor 27-inch",
        "category": "Electronics & Computers",
        "price": 38500.0,
        "stock": 18,
        "rating": 4.9,
        "description": "27-inch 4K IPS display with 144Hz refresh rate, 1ms response time, HDR400, and ultra-thin bezels. Perfect for gaming, coding, and creative editing."
    },
    {
        "id": 4,
        "name": "Vortex MechPro RGB Mechanical Keyboard",
        "category": "Electronics & Computers",
        "price": 5200.0,
        "stock": 35,
        "rating": 4.6,
        "description": "Customizable hot-swappable mechanical keyboard with tactile red switches, RGB backlit lighting, aluminum alloy frame, and detachable braided cable."
    },
    {
        "id": 5,
        "name": "PowerCore 20000mAh Ultra-Fast Power Bank",
        "category": "Mobile Accessories",
        "price": 2800.0,
        "stock": 85,
        "rating": 4.7,
        "description": "Heavy-duty 65W PD fast-charging portable power bank capable of charging smartphones, tablets, and laptops. Features digital battery display and multi-device ports."
    },
    {
        "id": 6,
        "name": "Zenith Ultra Slim 15.6-inch Laptop",
        "category": "Electronics & Computers",
        "price": 95000.0,
        "stock": 12,
        "rating": 4.8,
        "description": "High performance Intel Core i7 13th Gen laptop with 16GB RAM, 1TB NVMe SSD, backlit keyboard, all-day 12-hour battery, and aluminum unibody."
    },

    # --- WEARABLES & WATCHES ---
    {
        "id": 7,
        "name": "AeroFit Watch X Smart Fitness Tracker",
        "category": "Wearables & Smartwatches",
        "price": 6499.0,
        "stock": 50,
        "rating": 4.7,
        "description": "AMOLED always-on display smartwatch with 24/7 heart rate, SpO2 blood oxygen monitor, sleep tracker, 100+ sports modes, Bluetooth calling, and 10-day battery."
    },
    {
        "id": 8,
        "name": "Titan Chronograph Classic Leather Watch",
        "category": "Wearables & Fashion",
        "price": 7200.0,
        "stock": 25,
        "rating": 4.9,
        "description": "Elegant analog chronograph wristwatch with genuine Italian brown leather strap, sapphire crystal glass, 50m water resistance, and Japanese quartz movement."
    },

    # --- FOOTWEAR & APPAREL ---
    {
        "id": 9,
        "name": "AeroStride Ultralight Running Shoes",
        "category": "Footwear & Sports",
        "price": 4500.0,
        "stock": 60,
        "rating": 4.8,
        "description": "High-cushion athletic running sneakers designed with breathable flyknit mesh, responsive foam sole, anti-slip traction, and lightweight shock absorption."
    },
    {
        "id": 10,
        "name": "StreetVibe Oversized Heavyweight Cotton Hoodie",
        "category": "Fashion & Apparel",
        "price": 3200.0,
        "stock": 40,
        "rating": 4.6,
        "description": "Super cozy 400 GSM 100% organic French terry cotton oversized streetwear hoodie with kangaroo pocket and double-lined hood. Available in Black, Slate, and Sage."
    },
    {
        "id": 11,
        "name": "RuggedTrail Waterproof Hiking Boots",
        "category": "Footwear & Sports",
        "price": 8500.0,
        "stock": 22,
        "rating": 4.7,
        "description": "Durable all-terrain outdoor hiking shoes with waterproof Gore-Tex membrane, reinforced rubber toe cap, and high-grip Vibram rubber outsole."
    },
    {
        "id": 12,
        "name": "FlexForm Dry-Fit Gym Training Shirt",
        "category": "Fashion & Apparel",
        "price": 1400.0,
        "stock": 95,
        "rating": 4.5,
        "description": "Moisture-wicking athletic gym performance tee with 4-way stretch fabric, anti-odor technology, and flatlock ergonomic seams."
    },

    # --- EYEWEAR & ACCESSORIES ---
    {
        "id": 13,
        "name": "SuperShade Polarized Aviator Sunglasses",
        "category": "Eyewear & Accessories",
        "price": 1800.0,
        "stock": 55,
        "rating": 4.8,
        "description": "Classic polarized UV400 protective sunglasses with lightweight metallic frame, anti-glare scratch-resistant dark lenses, and protective hard leather case."
    },
    {
        "id": 14,
        "name": "NordicVoyage Anti-Theft Water-Resistant Laptop Backpack",
        "category": "Bags & Accessories",
        "price": 3900.0,
        "stock": 38,
        "rating": 4.8,
        "description": "Minimalist 25L commuter backpack with padded 16-inch laptop compartment, hidden anti-theft zipper, built-in USB charging port, and water-repellent fabric."
    },
    {
        "id": 15,
        "name": "Apex Minimalist RFID-Blocking Carbon Fiber Wallet",
        "category": "Bags & Accessories",
        "price": 1600.0,
        "stock": 65,
        "rating": 4.7,
        "description": "Slim aerospace-grade aluminum and carbon fiber front-pocket wallet with quick-access card ejector mechanism and money clip."
    },
    {
        "id": 16,
        "name": "HydraFlask Insulated Stainless Steel Water Bottle 1L",
        "category": "Sports & Kitchen",
        "price": 1500.0,
        "stock": 80,
        "rating": 4.9,
        "description": "Double-wall vacuum insulated thermo water bottle keeping drinks ice cold for 24 hours or piping hot for 12 hours. BPA-free leakproof lid with carry handle."
    },

    # --- HOME, KITCHEN & LIFESTYLE ---
    {
        "id": 17,
        "name": "BaristaPro Espresso & Cappuccino Coffee Machine",
        "category": "Home & Kitchen",
        "price": 24500.0,
        "stock": 15,
        "rating": 4.9,
        "description": "20-bar professional high-pressure Italian pump espresso maker with stainless steel steam wand for silky microfoam milk, 1.5L water tank, and cup warmer."
    },
    {
        "id": 18,
        "name": "CrispAir Digital XXL Air Fryer 6.5L",
        "category": "Home & Kitchen",
        "price": 14500.0,
        "stock": 28,
        "rating": 4.8,
        "description": "Oil-free rapid 360-degree air circulation fryer with 8 one-touch cooking presets, non-stick dishwasher-safe basket, and LED digital touchscreen."
    },
    {
        "id": 19,
        "name": "ErgoRest Ergonomic High-Back Mesh Office Chair",
        "category": "Furniture & Office",
        "price": 19500.0,
        "stock": 16,
        "rating": 4.8,
        "description": "Full orthopedic lumbar support executive desk chair with breathable mesh, 3D adjustable armrests, reclining backrest, and heavy-duty smooth casters."
    },
    {
        "id": 20,
        "name": "Lumina Aura Smart RGB Ambient Desk Lamp",
        "category": "Home & Lighting",
        "price": 3100.0,
        "stock": 48,
        "rating": 4.6,
        "description": "Modern minimalist cylinder LED smart mood lamp with 16 million colors, music rhythm sync, touch dimming, and Alexa/Google Home compatibility."
    },

    # --- BEAUTY & PERSONAL CARE ---
    {
        "id": 21,
        "name": "SonicGleam Pro Electric Ultrasonic Toothbrush",
        "category": "Personal Care",
        "price": 3600.0,
        "stock": 52,
        "rating": 4.7,
        "description": "40,000 VPM ultrasonic smart electric toothbrush with 5 brushing modes, 2-minute smart timer, wireless charging dock, and 4 replacement brush heads."
    },
    {
        "id": 22,
        "name": "TheraRelief Percussion Deep Tissue Massage Gun",
        "category": "Personal Care & Health",
        "price": 5800.0,
        "stock": 30,
        "rating": 4.8,
        "description": "Ultra-quiet handheld muscle therapy massage gun with 6 speed levels, 6 interchangeable massage heads, high-torque brushless motor, and carry case."
    },
    {
        "id": 23,
        "name": "PureGlow Organic Hyaluronic Acid & Vitamin C Serum",
        "category": "Personal Care & Beauty",
        "price": 1900.0,
        "stock": 75,
        "rating": 4.9,
        "description": "Anti-aging, brightening, and intense hydration face serum infused with pure botanical extracts, niacinamide, and aloe vera."
    }
]

SAMPLE_ORDERS = [
    {
        "id": 1001,
        "customer_id": 123,
        "status": "In Transit",
        "total_amount": 13499.0,
        "items_summary": "1x NovaPulse Pro Wireless Headphones, 1x AeroStride Running Shoes",
        "courier": "TCS Express / Tracking #PK-98214-X",
        "estimated_delivery": "Arriving Tomorrow by 5:00 PM"
    },
    {
        "id": 1002,
        "customer_id": 123,
        "status": "Out for Delivery",
        "total_amount": 1800.0,
        "items_summary": "1x SuperShade Polarized Aviator Sunglasses",
        "courier": "Leopard Courier / Tracking #LEO-44102-B",
        "estimated_delivery": "Out for delivery today with courier agent"
    },
    {
        "id": 1003,
        "customer_id": 123,
        "status": "Delivered",
        "total_amount": 24500.0,
        "items_summary": "1x BaristaPro Espresso & Cappuccino Coffee Machine",
        "courier": "BlueEx / Tracking #BX-77291-C",
        "estimated_delivery": "Delivered on Friday, signed by recipient"
    },
    {
        "id": 1004,
        "customer_id": 456,
        "status": "Processing",
        "total_amount": 6499.0,
        "items_summary": "1x AeroFit Watch X Smart Fitness Tracker",
        "courier": "Standard Courier (Packaging in warehouse)",
        "estimated_delivery": "Dispatches within 24 hours"
    },
    {
        "id": 1005,
        "customer_id": 123,
        "status": "In Transit",
        "total_amount": 7100.0,
        "items_summary": "1x Vortex MechPro RGB Keyboard, 1x PureGlow Vitamin C Serum",
        "courier": "DHL Express / Tracking #DHL-55201-P",
        "estimated_delivery": "Estimated delivery in 2 days"
    }
]
