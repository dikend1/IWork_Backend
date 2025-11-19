from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.review_model import ReviewModel
from app.schemas.review_schema import ReviewCreate,ReviewResponse,ReviewUpdate


class ReviewService:
    def __init__(self,db_session:AsyncSession):
        self.db = db_session
    

    async def create_review(self,review_data:ReviewCreate) -> ReviewModel:
        review = ReviewModel(**review_data.model_dump())
        self.db.add(review)
        await self.db.commit()
        await self.db.refresh(review)
        return review
    
    async def get_review(self,review_id:int)->ReviewModel:
        query = select(ReviewModel).where(ReviewModel.id == review_id)
        reslut = await self.db.execute(query)
        return reslut.scalar_one_or_none
    
    async def update_review(self,review_id:int,review_data:ReviewUpdate)->ReviewModel:
        review = await self.get_review(review_id)
        if not review:
            return None
        for field,value in review_data.model_dump(exclude_unset=True).items():
            setattr(review,field,value)
        
        await self.db.commit()
        await self.db.refresh(review)
        return review
    
    async def delete_review(self,review_id:int)->bool:
        review = await self.get_review(review_id)
        if not review:
            return False
        await self.db.delete(review)
        await self.db.commit()
        return True
        