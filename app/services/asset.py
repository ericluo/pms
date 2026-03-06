from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.asset import Asset
from app.schemas.asset import AssetCreate, AssetUpdate

class AssetService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_assets(self) -> List[Asset]:
        return self.db.query(Asset).all()
    
    def get_asset(self, asset_id: int) -> Optional[Asset]:
        return self.db.query(Asset).filter(Asset.id == asset_id).first()
    
    def get_asset_by_code(self, code: str) -> Optional[Asset]:
        return self.db.query(Asset).filter(Asset.code == code).first()
    
    def create_asset(self, asset_create: AssetCreate) -> Asset:
        db_asset = Asset(
            code=asset_create.code,
            name=asset_create.name,
            type=asset_create.type,
            market=asset_create.market,
            industry=asset_create.industry
        )
        self.db.add(db_asset)
        self.db.commit()
        self.db.refresh(db_asset)
        return db_asset
    
    def update_asset(self, asset_id: int, asset_update: AssetUpdate) -> Optional[Asset]:
        db_asset = self.get_asset(asset_id)
        if not db_asset:
            return None
        for key, value in asset_update.dict(exclude_unset=True).items():
            setattr(db_asset, key, value)
        self.db.commit()
        self.db.refresh(db_asset)
        return db_asset
    
    def delete_asset(self, asset_id: int) -> bool:
        db_asset = self.get_asset(asset_id)
        if not db_asset:
            return False
        self.db.delete(db_asset)
        self.db.commit()
        return True