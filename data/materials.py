from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import json
import os

@dataclass
class Material:
    """Class representing a construction material."""
    name: str
    category: str
    unit: str
    price: float
    created_at: datetime = datetime.now()

    def to_dict(self) -> Dict:
        """Convert Material to dictionary."""
        return {
            "name": self.name,
            "category": self.category,
            "unit": self.unit,
            "price": self.price,
            "created_at": self.created_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Material':
        """Create Material from dictionary."""
        return cls(
            name=data["name"],
            category=data["category"],
            unit=data["unit"],
            price=data["price"],
            created_at=datetime.fromisoformat(data["created_at"])
        )

# Материалы для пола
FLOOR_MATERIALS: Dict[str, Material] = {
    "laminate": Material(
        name="Ламинат",
        unit="м²",
        price=800,
        category="floor"
    ),
    "parquet": Material(
        name="Паркетная доска",
        unit="м²",
        price=2000,
        category="floor"
    ),
    "tile": Material(
        name="Керамическая плитка",
        unit="м²",
        price=1200,
        category="floor"
    )
}

# Материалы для стен
WALL_MATERIALS: Dict[str, Material] = {
    "wallpaper": Material(
        name="Обои",
        unit="м²",
        price=500,
        category="walls"
    ),
    "paint": Material(
        name="Краска",
        unit="м²",
        price=300,
        category="walls"
    ),
    "tile": Material(
        name="Керамическая плитка",
        unit="м²",
        price=1200,
        category="walls"
    )
}

# Материалы для потолка
CEILING_MATERIALS: Dict[str, Material] = {
    "paint": Material(
        name="Краска",
        unit="м²",
        price=300,
        category="ceiling"
    ),
    "stretch": Material(
        name="Натяжной потолок",
        unit="м²",
        price=1500,
        category="ceiling"
    )
}

# Объединяем все материалы в один словарь
ALL_MATERIALS: Dict[str, Dict[str, Material]] = {
    "floor": FLOOR_MATERIALS,
    "walls": WALL_MATERIALS,
    "ceiling": CEILING_MATERIALS
}

def get_materials_by_category(category: str) -> Dict[str, Material]:
    """Get materials by category."""
    return ALL_MATERIALS.get(category, {})

def get_material(category: str, material_id: str) -> Material:
    """Get specific material by category and ID."""
    return ALL_MATERIALS.get(category, {}).get(material_id)

def get_material_file_path(user_id: int) -> str:
    """Get path to user's materials file."""
    return f"data/users/{user_id}_materials.json"

def save_material(user_id: int, material: Material) -> None:
    """Save material to user's file."""
    file_path = get_material_file_path(user_id)
    materials = get_user_materials(user_id)
    materials.append(material)
    
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump([m.to_dict() for m in materials], f, ensure_ascii=False, indent=2)

def get_user_materials(user_id: int) -> List[Material]:
    """Get all materials for user."""
    file_path = get_material_file_path(user_id)
    if not os.path.exists(file_path):
        return []
    
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return [Material.from_dict(m) for m in data]

def format_material_info(material: Material) -> str:
    """Format material information for display."""
    return (
        f"📝 {material.name}\n"
        f"📋 Категория: {material.category}\n"
        f"📏 Единица измерения: {material.unit}\n"
        f"💰 Цена: {material.price} руб./{material.unit}\n"
        f"📅 Добавлено: {material.created_at.strftime('%d.%m.%Y %H:%M')}"
    ) 