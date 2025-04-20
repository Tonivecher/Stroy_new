from dataclasses import dataclass
from datetime import datetime
import json
import os
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

@dataclass
class Room:
    """Class representing a room."""
    name: str
    length: float
    width: float
    height: float
    area: float
    floor_area: float
    created_at: datetime

    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'length': self.length,
            'width': self.width,
            'height': self.height,
            'area': self.area,
            'floor_area': self.floor_area,
            'created_at': self.created_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Room':
        try:
            # If floor_area is not present, use the same value as area
            floor_area = data.get('floor_area', data['area'])
            # If height is not present, default to 2.5 meters (standard ceiling height)
            height = data.get('height', 2.5)
            return cls(
                name=data['name'],
                length=data['length'],
                width=data['width'],
                height=height,
                area=data['area'],
                floor_area=floor_area,
                created_at=datetime.fromisoformat(data['created_at'])
            )
        except Exception as e:
            logger.error(f"Error creating Room from dict: {e}")
            raise

def get_rooms_file(user_id: int) -> str:
    """Get the path to the user's rooms file."""
    try:
        os.makedirs('data/users', exist_ok=True)
        return f'data/users/{user_id}_rooms.json'
    except Exception as e:
        logger.error(f"Error getting rooms file: {e}")
        raise

def save_room(user_id: int, room: Room) -> None:
    """Save a room to the user's rooms file."""
    try:
        filename = get_rooms_file(user_id)
        rooms = get_user_rooms(user_id)
        rooms.append(room)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(
                [r.to_dict() for r in rooms],
                f,
                ensure_ascii=False,
                indent=2
            )
        logger.info(f"Room saved successfully for user {user_id}")
    except Exception as e:
        logger.error(f"Error saving room: {e}")
        raise

def get_user_rooms(user_id: int) -> List[Room]:
    """Get all rooms for a user."""
    try:
        filename = get_rooms_file(user_id)
        if not os.path.exists(filename):
            return []
        
        with open(filename, 'r', encoding='utf-8') as f:
            try:
                rooms_data = json.load(f)
                return [Room.from_dict(r) for r in rooms_data]
            except json.JSONDecodeError as e:
                logger.error(f"Error decoding JSON for user {user_id}: {e}")
                return []
    except Exception as e:
        logger.error(f"Error getting user rooms: {e}")
        return []

def format_room_info(room: Room) -> str:
    """Format room information for display."""
    try:
        return (
            f"🏠 {room.name}\n"
            f"📏 Длина: {room.length} м\n"
            f"📏 Ширина: {room.width} м\n"
            f"📏 Высота: {room.height} м\n"
            f"📐 Общая площадь: {room.area:.2f} м²\n"
            f"📐 Площадь пола: {room.floor_area:.2f} м²\n"
            f"📅 Добавлено: {room.created_at.strftime('%d.%m.%Y %H:%M')}\n"
        )
    except Exception as e:
        logger.error(f"Error formatting room info: {e}")
        return "Ошибка при форматировании информации о помещении" 