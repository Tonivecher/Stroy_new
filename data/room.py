from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Room:
    """Class representing a room with its measurements and materials."""
    name: str
    length: float
    width: float
    height: float = 2.7  # стандартная высота потолка
    created_at: datetime = datetime.now()
    
    @property
    def floor_area(self) -> float:
        """Calculate floor area."""
        return self.length * self.width
    
    @property
    def wall_area(self) -> float:
        """Calculate wall area."""
        return 2 * (self.length + self.width) * self.height
    
    @property
    def ceiling_area(self) -> float:
        """Calculate ceiling area."""
        return self.floor_area

class RoomEstimate:
    """Class for storing room estimate information."""
    def __init__(self, room: Room):
        self.room = room
        self.materials: Dict[str, Dict] = {
            "floor": {},
            "walls": {},
            "ceiling": {}
        }
    
    def add_material(self, category: str, material_id: str, quantity: float) -> None:
        """Add material to estimate."""
        self.materials[category][material_id] = quantity
    
    def calculate_total_cost(self) -> Dict[str, float]:
        """Calculate total cost of materials and work."""
        from data.materials import get_material
        
        total_materials_cost = 0
        total_work_cost = 0
        
        for category, materials in self.materials.items():
            for material_id, quantity in materials.items():
                material = get_material(category, material_id)
                if material:
                    total_materials_cost += material.price_per_unit * quantity
                    total_work_cost += material.work_price_per_unit * quantity
        
        return {
            "materials": total_materials_cost,
            "work": total_work_cost,
            "total": total_materials_cost + total_work_cost
        }
    
    def format_estimate(self) -> str:
        """Format estimate information for display."""
        from data.materials import get_material
        
        result = [
            f"🏠 <b>{self.room.name}</b>",
            f"📏 Размеры: {self.room.length} x {self.room.width} м",
            f"📐 Площадь пола: {self.room.floor_area:.2f} м²",
            f"🧱 Площадь стен: {self.room.wall_area:.2f} м²",
            f"🪟 Площадь потолка: {self.room.ceiling_area:.2f} м²",
            "\n<b>Материалы:</b>"
        ]
        
        for category, materials in self.materials.items():
            if materials:
                result.append(f"\n<b>{category.capitalize()}:</b>")
                for material_id, quantity in materials.items():
                    material = get_material(category, material_id)
                    if material:
                        cost = material.price_per_unit * quantity
                        work_cost = material.work_price_per_unit * quantity
                        result.append(
                            f"- {material.name}: {quantity} {material.unit}\n"
                            f"  Материалы: {cost:.2f} ₽\n"
                            f"  Работы: {work_cost:.2f} ₽"
                        )
        
        costs = self.calculate_total_cost()
        result.extend([
            "\n<b>Итого:</b>",
            f"Материалы: {costs['materials']:.2f} ₽",
            f"Работы: {costs['work']:.2f} ₽",
            f"<b>Всего: {costs['total']:.2f} ₽</b>"
        ])
        
        return "\n".join(result) 