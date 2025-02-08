from PyQt6.QtWidgets import (
    QApplication, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget,
    QStackedLayout, QSizePolicy, QLineEdit, QGridLayout, QGroupBox, QRadioButton, QButtonGroup
)
from PyQt6.QtCore import Qt, QEvent
import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("본1-부 계산기")
        self.resize(800, 600)
        self.stacked_layout = QStackedLayout()
        self.raid_type = 0
        self.selected_sub = "부1"  # ✅ 기본값 "부1"
        self.pot_label = QLabel("파티당 폿 2개를 맞춰야 합니다.")  # 초기값 (부1 선택 상태)
        self.pot_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.initUI()
        self.installEventFilter(self)  # ✅ 마우스 뒤로가기 필터 등록

    def initUI(self):
        self.page0 = self.create_main_page()
        self.page4 = self.create_raid_page(1)

        self.stacked_layout.addWidget(self.page0)
        self.stacked_layout.addWidget(self.page4)

        self.setLayout(self.stacked_layout)
        self.stacked_layout.setCurrentIndex(0)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Back:
            self.goBack()
            return True
        if event.type() == QEvent.Type.MouseButtonPress and event.button() == Qt.MouseButton.BackButton:
            self.goBack()
            return True
        return super().eventFilter(obj, event)

    def goBack(self):
        current_index = self.stacked_layout.currentIndex()
        if current_index > 0:
            self.stacked_layout.setCurrentIndex(0)
    def update_raid_type(self, raid_type):
        self.raid_type = raid_type  # 값 변경
        # print(self.raid_type , self.selected_sub)  # 변경 후 값 출력
    
    def create_main_page(self):
        layout = QVBoxLayout()
        label = QLabel("본1 부 계산기 입니다!")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hbox = QHBoxLayout()
        startButton = QPushButton("시작")

        self.setupButton(startButton)

        startButton.clicked.connect(lambda: self.stacked_layout.setCurrentIndex(1))
        startButton.clicked.connect(lambda: self.update_raid_type(4))

        hbox.addWidget(startButton)

        layout.addWidget(label)
        layout.addLayout(hbox)

        page = QWidget()
        page.setLayout(layout)
        return page

    def create_raid_page(self, party_count):
        layout = QVBoxLayout()

        # ✅ "선택된 레이드: {}" 오른쪽에 라디오 버튼 배치
        raid_type_layout = QHBoxLayout()
        sub_char_layout = QHBoxLayout()

        # ✅ 라디오 버튼 추가
        self.radio0_group = QButtonGroup(self)
        self.radio0_4 = QRadioButton("4인")
        self.radio0_8 = QRadioButton("8인")
        self.radio0_16 = QRadioButton("16인")
        self.radio0_4.setChecked(True)  # 기본 선택값 "4인"

        self.radio0_group.addButton(self.radio0_4)
        self.radio0_group.addButton(self.radio0_8)
        self.radio0_group.addButton(self.radio0_16)
        self.radio0_group.setExclusive(True)

        self.radio1_group = QButtonGroup(self)
        self.radio1_1 = QRadioButton("부1")
        self.radio1_3 = QRadioButton("부3")
        self.radio1_1.setChecked(True)  # 기본 선택값 "부1"

        self.radio1_group.addButton(self.radio1_1)
        self.radio1_group.addButton(self.radio1_3)
        self.radio1_group.setExclusive(True)
        
        self.radio0_4.toggled.connect(lambda checked: self.update_raid_type(4) if checked else None)
        self.radio0_8.toggled.connect(lambda checked: self.update_raid_type(8) if checked else None)
        self.radio0_16.toggled.connect(lambda checked: self.update_raid_type(16) if checked else None)

        self.radio1_1.toggled.connect(lambda checked: self.set_sub_choice("부1") if checked else None)
        self.radio1_3.toggled.connect(lambda checked: self.set_sub_choice("부3") if checked else None)


        # ✅ 라디오 버튼을 오른쪽에 배치
        radio0_layout = QHBoxLayout()
        radio0_layout.addWidget(self.radio0_4)
        radio0_layout.addWidget(self.radio0_8)
        radio0_layout.addWidget(self.radio0_16)
        raid_type_layout.addLayout(radio0_layout)
        raid_type_layout.addStretch()

        radio1_layout = QHBoxLayout()
        radio1_layout.addWidget(self.radio1_1)
        radio1_layout.addWidget(self.radio1_3)
        sub_char_layout.addLayout(radio1_layout)  # "선택된 레이드" 오른쪽에 추가
        sub_char_layout.addStretch()
        
        top_bar = QHBoxLayout()
        home_button = QPushButton("홈으로")
        back_button = QPushButton("뒤로가기")
        calc_button = QPushButton("계산")
        calc_button.setEnabled(False)

        home_button.clicked.connect(self.resetApp)
        back_button.clicked.connect(self.goBack)

        top_bar.addWidget(home_button)
        top_bar.addWidget(back_button)
        top_bar.addStretch()
        top_bar.addWidget(calc_button)

        layout.addLayout(top_bar)
        layout.addLayout(raid_type_layout)  # ✅ "선택된 레이드" + 라디오 버튼
        layout.addLayout(sub_char_layout)  # ✅ "선택된 레이드" + 라디오 버튼
        layout.addWidget(self.pot_label)  # ✅ 폿 문구 추가
        layout.addLayout(self.create_party_layout(party_count, calc_button))

        page = QWidget()
        page.setLayout(layout)
        return page

    def update_pot_notice(self, choice):
        """✅ 선택한 부에 따라 폿 안내 문구 변경"""
        if choice == "부1":
            self.pot_label.setText("파티당 폿 2개를 맞춰야 합니다.")
        else:
            self.pot_label.setText("파티당 폿 4개를 맞춰야 합니다.")

    def set_sub_choice(self, choice):
        print(choice)  # 선택한 부 출력
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
        self.selected_sub = "부1"  # 기본값 초기화
        self.radio1.setChecked(True)  # 기본값을 부1로 초기화
        self.stacked_layout.setCurrentIndex(0)

    def setupButton(self, button):
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        button.setMaximumHeight(300)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())