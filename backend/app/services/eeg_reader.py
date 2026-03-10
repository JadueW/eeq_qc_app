from pathlib import Path

import mne
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.task_manager import update_task
from app.db.models import Channel, EEGFile


def parse_eeg_file_task(task_id: str, file_id: int) -> None:
    """
    后台任务：解析EEG文件

    1 读取文件
    2 获取基本信息
    3 写入channels表
    4 更新文件状态
    """

    db: Session = SessionLocal()

    try:
        update_task(db, task_id, status="running", progress=5, message="开始解析文件")

        eeg_file = db.query(EEGFile).filter(EEGFile.id == file_id).first()

        if not eeg_file:
            raise ValueError("文件不存在")

        eeg_file.status = "parsing"
        db.commit()

        file_path = Path(eeg_file.stored_path)

        # 使用MNE自动识别格式
        raw = mne.io.read_raw(file_path, preload=False, verbose="ERROR")

        update_task(db, task_id, progress=30, message="读取文件头完成")

        sfreq = float(raw.info["sfreq"])
        ch_names = raw.ch_names
        n_channels = len(ch_names)
        duration_sec = raw.n_times / sfreq

        eeg_file.sampling_rate = sfreq
        eeg_file.n_channels = n_channels
        eeg_file.duration_sec = duration_sec
        eeg_file.format = file_path.suffix.lower().replace(".", "")
        eeg_file.status = "parsed"

        db.commit()

        # 删除旧通道
        db.query(Channel).filter(Channel.file_id == eeg_file.id).delete()
        db.commit()

        # 插入通道
        for idx, ch_name in enumerate(ch_names):

            ch_type = raw.get_channel_types(picks=[idx])[0]

            channel = Channel(
                file_id=eeg_file.id,
                channel_index=idx,
                name=ch_name,
                type=ch_type,
                status="good",
            )

            db.add(channel)

        db.commit()

        update_task(db, task_id, progress=100, status="done", message="解析完成")

    except Exception as e:

        file_obj = db.query(EEGFile).filter(EEGFile.id == file_id).first()

        if file_obj:
            file_obj.status = "error"
            file_obj.error_message = str(e)
            db.commit()

        update_task(db, task_id, status="error", error_message=str(e))

    finally:
        db.close()