from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.asset import Asset, ASSET_TYPES
from app.schemas.asset import AssetCreate, AssetUpdate

class AssetService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_assets(self, asset_type: str = None, market: str = None) -> List[Asset]:
        query = self.db.query(Asset)
        if asset_type:
            query = query.filter(Asset.type == asset_type)
        if market:
            query = query.filter(Asset.market == market)
        return query.all()
    
    def get_asset(self, asset_id: int) -> Optional[Asset]:
        return self.db.query(Asset).filter(Asset.id == asset_id).first()
    
    def get_asset_by_code(self, code: str) -> Optional[Asset]:
        return self.db.query(Asset).filter(Asset.code == code).first()
    
    def create_asset(self, asset_data: dict) -> Asset:
        db_asset = Asset(
            code=asset_data.get('code'),
            name=asset_data.get('name'),
            type=asset_data.get('type'),
            market=asset_data.get('market'),
            industry=asset_data.get('industry'),
            interest_rate=asset_data.get('interest_rate')
        )
        self.db.add(db_asset)
        self.db.commit()
        self.db.refresh(db_asset)
        return db_asset
    
    def update_asset(self, asset_id: int, asset_data: dict) -> Optional[Asset]:
        db_asset = self.get_asset(asset_id)
        if not db_asset:
            return None
        for key, value in asset_data.items():
            if value is not None:
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
    
    def get_asset_types(self) -> List[dict]:
        return [{'value': t, 'label': self._get_type_name(t)} for t in ASSET_TYPES]
    
    def _get_type_name(self, asset_type: str) -> str:
        names = {
            'stock': '股票',
            'fund': '基金',
            'bond': '债券',
            'cash': '现金'
        }
        return names.get(asset_type, asset_type)