from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Goal
from app.schemas.goal import GoalCreate, GoalUpdate, GoalContribute, GoalResponse

router = APIRouter()


def goal_to_response(goal: Goal) -> dict:
    progress = (goal.current_amount / goal.target_amount * 100) if goal.target_amount > 0 else 0
    days_remaining = (goal.deadline - date.today()).days
    return {
        "id": goal.id,
        "name": goal.name,
        "target_amount": goal.target_amount,
        "current_amount": goal.current_amount,
        "deadline": goal.deadline,
        "created_at": goal.created_at,
        "progress_percentage": round(progress, 1),
        "days_remaining": max(0, days_remaining)
    }


@router.get("", response_model=list[GoalResponse])
def list_goals(db: Session = Depends(get_db)):
    goals = db.query(Goal).all()
    return [goal_to_response(g) for g in goals]


@router.post("", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
def create_goal(data: GoalCreate, db: Session = Depends(get_db)):
    goal = Goal(**data.model_dump())
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return goal_to_response(goal)


@router.put("/{goal_id}", response_model=GoalResponse)
def update_goal(goal_id: int, data: GoalUpdate, db: Session = Depends(get_db)):
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(goal, key, value)

    db.commit()
    db.refresh(goal)
    return goal_to_response(goal)


@router.post("/{goal_id}/contribute", response_model=GoalResponse)
def contribute_to_goal(goal_id: int, data: GoalContribute, db: Session = Depends(get_db)):
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")

    goal.current_amount += data.amount
    db.commit()
    db.refresh(goal)
    return goal_to_response(goal)


@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_goal(goal_id: int, db: Session = Depends(get_db)):
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")

    db.delete(goal)
    db.commit()
