from PyQt6.QtWidgets import (
    QApplication, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget,
    QStackedLayout, QSizePolicy, QLineEdit, QGridLayout, QGroupBox, QRadioButton, QButtonGroup
)
from PyQt6.QtCore import Qt
import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("본1-부 계산기")
        self.resize(800, 600)
        self.stacked_layout = QStackedLayout()
        self.raid_type = 1
        self.selected_sub = "부1"  # ✅ 기본값 "부1"
        self.pot_label = QLabel("파티당 폿 2개씩 맞춰야 합니다.")  # 초기값 (부1 선택 상태)
        self.pot_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.initUI()

    def initUI(self):
        self.main_page = self.create_main_page()
        self.raid_page = self.create_raid_page(1)

        self.stacked_layout.addWidget(self.main_page)
        self.stacked_layout.addWidget(self.raid_page)

        self.setLayout(self.stacked_layout)
        self.stacked_layout.setCurrentIndex(0)

    def update_raid_type(self, raid_type):
        """✅ 기존과 다른 레이드 타입일 때만 변경"""
        if self.raid_type != raid_type:
            self.raid_type = raid_type  # 값 변경
            self.update_raid_page(raid_type)

    def create_main_page(self):
        layout = QVBoxLayout()
        label = QLabel("본1 부 계산기 입니다!")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hbox = QHBoxLayout()
        startButton = QPushButton("시작")

        self.setupButton(startButton)

        startButton.clicked.connect(lambda: self.stacked_layout.setCurrentIndex(1))
        startButton.clicked.connect(lambda: self.update_raid_type(1))

        hbox.addWidget(startButton)

        layout.addWidget(label)
        layout.addLayout(hbox)

        page = QWidget()
        page.setLayout(layout)
        return page
    
    def create_raid_page(self, party_count):
        layout = QVBoxLayout()
        resetButton = QPushButton("초기화")
        resetButton.clicked.connect(self.resetApp)

        # ✅ 버튼을 클래스 속성으로 저장
        self.calc_button = QPushButton("계산")
        self.calc_button.setEnabled(False)  # 기본적으로 비활성화

        # ✅ 기존 시그널 제거 (연결된 경우만 disconnect)
        for btn in ["radio0_4", "radio0_8", "radio0_16", "radio1_1", "radio1_3"]:
            if hasattr(self, btn):
                try:
                    getattr(self, btn).toggled.disconnect()
                except TypeError:
                    pass  # 연결이 없으면 예외 무시

        # ✅ 기존 `radio0_group`이 없으면 새로 생성
        if not hasattr(self, "radio0_group"):
            self.radio0_group = QButtonGroup(self)
            self.radio0_4 = QRadioButton("4인")
            self.radio0_8 = QRadioButton("8인")
            self.radio0_16 = QRadioButton("16인")
            self.radio0_4.setChecked(True)  # 기본 선택값 "4인"

            self.radio0_group.addButton(self.radio0_4)
            self.radio0_group.addButton(self.radio0_8)
            self.radio0_group.addButton(self.radio0_16)
            self.radio0_group.setExclusive(True)

        # ✅ 기존 `radio1_group`이 없으면 새로 생성
        if not hasattr(self, "radio1_group"):
            self.radio1_group = QButtonGroup(self)
            self.radio1_1 = QRadioButton("부1")
            self.radio1_3 = QRadioButton("부3")
            self.radio1_1.setChecked(True)  # 기본 선택값 "부1"

            self.radio1_group.addButton(self.radio1_1)
            self.radio1_group.addButton(self.radio1_3)
            self.radio1_group.setExclusive(True)

        # ✅ 레이드 선택 버튼 이벤트 연결
        self.radio0_4.toggled.connect(lambda checked: self.update_raid_type(1) if checked else None)
        self.radio0_8.toggled.connect(lambda checked: self.update_raid_type(2) if checked else None)
        self.radio0_16.toggled.connect(lambda checked: self.update_raid_type(4) if checked else None)

        self.radio1_1.toggled.connect(lambda checked: self.set_sub_choice("부1") if checked else None)
        self.radio1_3.toggled.connect(lambda checked: self.set_sub_choice("부3") if checked else None)

        # ✅ UI 레이아웃 배치
        top_bar = QHBoxLayout()
        top_bar.addStretch()
        top_bar.addWidget(resetButton) 
        top_bar.addWidget(self.calc_button)
        layout.addLayout(top_bar)

        radio0_layout = QHBoxLayout()
        radio0_layout.addWidget(self.radio0_4)
        radio0_layout.addWidget(self.radio0_8)
        radio0_layout.addWidget(self.radio0_16)

        radio1_layout = QHBoxLayout()
        radio1_layout.addWidget(self.radio1_1)
        radio1_layout.addWidget(self.radio1_3)

        layout.addLayout(radio0_layout)
        layout.addLayout(radio1_layout)
        layout.addWidget(self.pot_label)  # ✅ 폿 문구 추가

        # ✅ 기존 페이지가 있으면 `create_party_layout`만 업데이트
        basic_raid_layout = self.create_party_layout(party_count, self.calc_button)
        layout.addLayout(basic_raid_layout)

        page = QWidget()
        page.setLayout(layout)
        return page

    def update_raid_page(self, raid_type):
        # ✅ 기존 `raid_page`가 존재하면 완전히 삭제
        if self.raid_page is not None:
            if self.stacked_layout.indexOf(self.raid_page) != -1:
                self.stacked_layout.removeWidget(self.raid_page)  # 스택에서 제거

            self.raid_page.deleteLater()  # 메모리에서 안전하게 삭제
            self.raid_page = None  # 참조 제거
            QApplication.processEvents()  # ✅ PyQt의 이벤트 루프를 강제로 실행해 삭제를 즉시 반영

        # ✅ 새로운 `raid_page` 생성
        self.raid_page = self.create_raid_page(raid_type)

        # ✅ 새로운 `raid_page`를 스택에 추가 및 활성화
        self.stacked_layout.addWidget(self.raid_page)
        self.stacked_layout.setCurrentWidget(self.raid_page)

    def update_pot_notice(self, choice):
        """✅ 선택한 부에 따라 폿 안내 문구 변경"""
        if choice == "부1":
            self.pot_label.setText("파티당 폿 2개씩 맞춰야 합니다.")
        else:
            self.pot_label.setText("파티당 폿 4개씩 맞춰야 합니다.")

    def set_sub_choice(self, choice):
        self.selected_sub = choice 
        self.update_pot_notice(choice=choice)

    def create_party_layout(self, party_count, calc_button):
        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)
        input_fields = []

        def check_all_filled():
            calc_button.setEnabled(all(field.text().strip() for field in input_fields))

        for party_idx in range(party_count):
            party_box = QVBoxLayout()
            party_label = QLabel(f"{party_idx + 1}파티")
            party_group = QGroupBox()
            party_layout = QVBoxLayout()

            for i in range(4):
                field_layout = QHBoxLayout()
                input_field = QLineEdit()
                name_field = QLineEdit()

                input_field.setPlaceholderText(f"{party_idx * 4 + i + 1}의 본부 입력")
                name_field.setPlaceholderText(f"{party_idx * 4 + i + 1}의 닉네임 입력")

                # ✅ 입력 필드 너비 설정
                input_field.setFixedWidth(100)
                name_field.setFixedWidth(150)

                # ✅ 입력 필드 중앙 정렬
                input_field.setAlignment(Qt.AlignmentFlag.AlignCenter)
                name_field.setAlignment(Qt.AlignmentFlag.AlignCenter)

                input_field.textChanged.connect(check_all_filled)
                input_fields.append(input_field)

                field_layout.addWidget(input_field)
                field_layout.addWidget(name_field)
                party_layout.addLayout(field_layout)

            party_group.setLayout(party_layout)
            party_box.addWidget(party_label)
            party_box.addWidget(party_group)
            grid_layout.addLayout(party_box, party_idx // 2, party_idx % 2)

        return grid_layout

    def resetApp(self):
        """✅ 입력 필드 초기화 및 기본 상태로 복구"""
        if self.raid_page is not None:
            # ✅ `raid_page` 내의 모든 입력 필드(`QLineEdit`) 초기화
            for widget in self.raid_page.findChildren(QLineEdit):
                widget.clear()
        # ✅ "계산" 버튼 다시 비활성화
        self.calc_button.setEnabled(False)

    def setupButton(self, button):
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        button.setMaximumHeight(300)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())