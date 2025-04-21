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

def update_room_name(user_id: int, room: Room, new_name: str) -> None:
    """Update the name of a room."""
    try:
        filename = get_rooms_file(user_id)
        rooms = get_user_rooms(user_id)
        
        # Find the room with the same name and update it
        for i, r in enumerate(rooms):
            if r.name == room.name:
                rooms[i].name = new_name
                break
        
        # Save updated rooms list
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(
                [r.to_dict() for r in rooms],
                f,
                ensure_ascii=False,
                indent=2
            )
        logger.info(f"Room name updated for user {user_id}: {room.name} -> {new_name}")
    except Exception as e:
        logger.error(f"Error updating room name: {e}")
        raise

def update_room_dimensions(user_id: int, room: Room, length: float, width: float, height: float) -> None:
    """Update the dimensions of a room."""
    try:
        filename = get_rooms_file(user_id)
        rooms = get_user_rooms(user_id)
        
        # Find the room with the same name and update its dimensions
        for i, r in enumerate(rooms):
            if r.name == room.name:
                # Calculate new areas
                total_area = 2 * (length + width) * height + 2 * (length * width)
                floor_area = length * width
                
                # Update room properties
                rooms[i].length = length
                rooms[i].width = width
                rooms[i].height = height
                rooms[i].area = total_area
                rooms[i].floor_area = floor_area
                break
        
        # Save updated rooms list
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(
                [r.to_dict() for r in rooms],
                f,
                ensure_ascii=False,
                indent=2
            )
        logger.info(f"Room dimensions updated for user {user_id}, room: {room.name}")
    except Exception as e:
        logger.error(f"Error updating room dimensions: {e}")
        raise

def delete_room(user_id: int, room: Room) -> None:
    """Delete a room from user's rooms list."""
    try:
        filename = get_rooms_file(user_id)
        rooms = get_user_rooms(user_id)
        
        # Remove room with the same name
        rooms = [r for r in rooms if r.name != room.name]
        
        # Save updated rooms list
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(
                [r.to_dict() for r in rooms],
                f,
                ensure_ascii=False,
                indent=2
            )
        logger.info(f"Room deleted for user {user_id}: {room.name}")
    except Exception as e:
        logger.error(f"Error deleting room: {e}")
        raise 