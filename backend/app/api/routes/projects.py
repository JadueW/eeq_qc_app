from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.response import ok
from app.db.models import Project
from app.schemas.project import ProjectCreate, ProjectOut

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.get("")
def list_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).order_by(Project.created_at.desc()).all()
    return ok([ProjectOut.model_validate(p).model_dump() for p in projects])


@router.post("")
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)):
    exists = db.query(Project).filter(Project.name == payload.name).first()
    if exists:
        raise HTTPException(status_code=400, detail="项目名已存在")

    project = Project(name=payload.name, description=payload.description)
    db.add(project)
    db.commit()
    db.refresh(project)
    return ok(ProjectOut.model_validate(project).model_dump(), "创建成功")


@router.get("/{project_id}")
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")

    files = []
    for f in project.files:
        files.append(
            {
                "id": f.id,
                "original_name": f.original_name,
                "status": f.status,
                "sampling_rate": f.sampling_rate,
                "n_channels": f.n_channels,
                "duration_sec": f.duration_sec,
                "created_at": f.created_at.isoformat(),
            }
        )

    return ok(
        {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "files": files,
        }
    )


@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")

    db.delete(project)
    db.commit()
    return ok(message="删除成功")