from fastapi import APIRouter, Depends, Query, HttpException
from sqlmodel import Session, select, func
from models import Review, ReviewCreate, ReviewRead, ReviewUpdate
from database import get_session

router = APIRouter(prefix='/review', tags=['review'])

@router.post("/", response_model=ReviewRead)
def create_review(review: ReviewCreate, session: Session = Depends(get_session)):
    new_review = Review.from_orm(review)
    session.add(new_review)
    session.commit()
    session.refresh(new_review)
    return new_review


@router.get("/", response_model=list[ReviewRead])
def list_reviews(
    session: Session = Depends(get_session),
    play_name: str | None  = Query(default=None, description="Filter by play name"),
    skip: int = Query(default=0, ge=0, description="Number of reviews to skip"),
    limit: int = Query(default=10, ge=1, le=50, description="Maximum number of reviews to return"),
    ):
    query = select(Review)
    if play_name:
        query = query.where(Review.play_name == play_name)
    query = query.offset(skip).limit(limit)
    reviews = session.exec(query).all()
    return reviews


@router.get("/average/{play_name}")
def get_average_rating(play_name: str, session: Session = Depends(get_session)):
    result = session.exec(select(func.avg(Review.rating)).where(Review.play_name == play_name)).first()
    avg_rating, total_reviews = result

    if total_reviews == 0:
        raise HttpException(status_code=404, detail="No reviews found for this play.")
    return {"play_name": play_name, "average_rating": round (avg_rating, 2), "total_reviews": total_reviews}


@router.patch('/{review_id}', response_model=ReviewRead)
def update_review(review_id: int, update: ReviewUpdate, session: Session = Depends(get_session)):
    review = session.get(Review, review_id)
    if not review:
        raise HttpException(status_code=404, detail="Review not found.")

    update_data = update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(review, key, value)
    
    session.add(review)
    session.commit() 
    session.refresh(review)
    return review

@router.delete('/{review_id}')
def delete_review(review_id: int, session: Session = Depends(get_session)):
    review = session.get(Review, review_id)
    if not review:
        raise HttpException(status_code=404, detail="Review not found.")
    
    session.delete(review)
    session.commit()
    return {"message": "Review deleted successfully."}