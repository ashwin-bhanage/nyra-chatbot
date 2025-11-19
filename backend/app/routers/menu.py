"""
Menu Router - API endpoints for menu operations
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.menu import MenuItem, MenuCategory
from app.schemas.menu import MenuItemResponse, MenuItemList, MenuItemCreate, MenuItemUpdate

# Create router instance
router = APIRouter()


@router.get("/menu", response_model=MenuItemList)
async def get_menu(
    category: Optional[str] = Query(None, description="Filter by category: appetizer, main, dessert, beverage"),
    available_only: bool = Query(True, description="Show only available items"),
    db: Session = Depends(get_db)
):
    """
    Get all menu items

    - **category**: Filter by category (optional)
    - **available_only**: Show only available items (default: true)

    Returns list of menu items with total count
    """
    # Start with base query
    query = db.query(MenuItem)

    # Filter by availability
    if available_only:
        query = query.filter(MenuItem.is_available == True)

    # Filter by category if provided
    if category:
        # Validate category
        try:
            category_enum = MenuCategory(category.lower())
            query = query.filter(MenuItem.category == category_enum)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid category. Must be one of: appetizer, main, dessert, beverage"
            )

    # Execute query
    items = query.all()

    # Convert to response format
    item_responses = []
    for item in items:
        item_responses.append(MenuItemResponse(
            id=item.id,
            name=item.name,
            description=item.description,
            category=item.category.value,
            price=item.price,
            is_available=item.is_available,
            image_url=item.image_url,
            created_at=item.created_at.isoformat() if item.created_at else ""
        ))

    return MenuItemList(
        items=item_responses,
        total=len(item_responses),
        category=category
    )


@router.get("/menu/{item_id}", response_model=MenuItemResponse)
async def get_menu_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    """
    Get specific menu item by ID

    - **item_id**: Menu item ID

    Returns single menu item or 404 if not found
    """
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()

    if not item:
        raise HTTPException(
            status_code=404,
            detail=f"Menu item with ID {item_id} not found"
        )

    return MenuItemResponse(
        id=item.id,
        name=item.name,
        description=item.description,
        category=item.category.value,
        price=item.price,
        is_available=item.is_available,
        image_url=item.image_url,
        created_at=item.created_at.isoformat() if item.created_at else ""
    )


@router.get("/menu/category/{category}", response_model=MenuItemList)
async def get_menu_by_category(
    category: str,
    available_only: bool = Query(True),
    db: Session = Depends(get_db)
):
    """
    Get menu items by category

    - **category**: appetizer, main, dessert, or beverage
    - **available_only**: Show only available items

    Returns list of items in that category
    """
    # Validate and convert category
    try:
        category_enum = MenuCategory(category.lower())
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid category '{category}'. Must be one of: appetizer, main, dessert, beverage"
        )

    # Query items
    query = db.query(MenuItem).filter(MenuItem.category == category_enum)

    if available_only:
        query = query.filter(MenuItem.is_available == True)

    items = query.all()

    # Convert to response
    item_responses = []
    for item in items:
        item_responses.append(MenuItemResponse(
            id=item.id,
            name=item.name,
            description=item.description,
            category=item.category.value,
            price=item.price,
            is_available=item.is_available,
            image_url=item.image_url,
            created_at=item.created_at.isoformat() if item.created_at else ""
        ))

    return MenuItemList(
        items=item_responses,
        total=len(item_responses),
        category=category
    )


@router.get("/menu/search/{search_term}", response_model=MenuItemList)
async def search_menu(
    search_term: str,
    db: Session = Depends(get_db)
):
    """
    Search menu items by name or description

    - **search_term**: Text to search for

    Returns matching items
    """
    # Search in name and description
    items = db.query(MenuItem).filter(
        (MenuItem.name.ilike(f"%{search_term}%")) |
        (MenuItem.description.ilike(f"%{search_term}%"))
    ).all()

    # Convert to response
    item_responses = []
    for item in items:
        item_responses.append(MenuItemResponse(
            id=item.id,
            name=item.name,
            description=item.description,
            category=item.category.value,
            price=item.price,
            is_available=item.is_available,
            image_url=item.image_url,
            created_at=item.created_at.isoformat() if item.created_at else ""
        ))

    return MenuItemList(
        items=item_responses,
        total=len(item_responses),
        category=None
    )


# Admin endpoint - create menu item (we'll add authentication later)
@router.post("/menu", response_model=MenuItemResponse, status_code=201)
async def create_menu_item(
    item: MenuItemCreate,
    db: Session = Depends(get_db)
):
    """
    Create new menu item (Admin only - will add auth later)

    - **item**: Menu item data

    Returns created menu item
    """
    # Validate category
    try:
        category_enum = MenuCategory(item.category.lower())
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid category. Must be one of: appetizer, main, dessert, beverage"
        )

    # Create new menu item
    new_item = MenuItem(
        name=item.name,
        description=item.description,
        category=category_enum,
        price=item.price,
        is_available=item.is_available,
        image_url=item.image_url
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return MenuItemResponse(
        id=new_item.id,
        name=new_item.name,
        description=new_item.description,
        category=new_item.category.value,
        price=new_item.price,
        is_available=new_item.is_available,
        image_url=new_item.image_url,
        created_at=new_item.created_at.isoformat() if new_item.created_at else ""
    )
