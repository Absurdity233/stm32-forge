import json
from pathlib import Path

from stm32_forge.ioc import import_ioc, read_ioc, write_ioc


def test_ioc_roundtrip(tmp_path: Path):
    source = tmp_path / "target.json"
    source.write_text(json.dumps({"mcu.Mcu": "STM32F103C8Tx", "RCC.APB1Freq_Value": 36000000}), encoding="utf-8")
    out = tmp_path / "project.ioc"
    write_ioc(out, json.loads(source.read_text()))
    values = read_ioc(out)
    assert values["mcu.Mcu"] == "STM32F103C8Tx"
    assert import_ioc(out)["device"] == "STM32F103C8Tx"
