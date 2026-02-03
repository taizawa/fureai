#!/usr/bin/env python3
"""
川崎市ふれあいネット 抽選申込アプリ
8件の申込設定をGUIで管理（PyQt5版）
"""

import sys
import json
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QLineEdit, QComboBox, QCheckBox, QPushButton,
    QGroupBox, QMessageBox, QFrame, QScrollArea, QListWidget, QListWidgetItem,
    QAbstractItemView, QSplitter, QDialog, QFormLayout, QDialogButtonBox,
    QFileDialog, QTableWidget, QTableWidgetItem, QHeaderView, QProgressDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import csv

# デフォルトアカウントデータ（Excelから取得）
DEFAULT_ACCOUNTS = [
    {'num': 1, 'name': '逢沢　雄也', 'nickname': 'ようた', 'id': '1357703', 'password': '1983', 'security': ''},
    {'num': 2, 'name': '刈谷　信士', 'nickname': 'はじめ', 'id': '1352189', 'password': '2023', 'security': ''},
    {'num': 3, 'name': '高橋　綾野', 'nickname': 'ひろゆき', 'id': '1363744', 'password': '0310', 'security': ''},
    {'num': 4, 'name': '芦澤　宏明', 'nickname': 'あおい', 'id': '1337287', 'password': '2512', 'security': ''},
    {'num': 5, 'name': '大坪　和恵', 'nickname': 'そうと', 'id': '1350494', 'password': '0013', 'security': 'rfc0013'},
    {'num': 6, 'name': '香取　美穂', 'nickname': 'たすく', 'id': '1311162', 'password': '0720', 'security': ''},
    {'num': 7, 'name': '一戸　花菜', 'nickname': 'そうすけ', 'id': '1352358', 'password': '0819', 'security': 'ichinohe'},
    {'num': 8, 'name': '一戸　健作', 'nickname': 'しゅうじ', 'id': '7002617', 'password': '1206', 'security': 'ichinohe'},
    {'num': 9, 'name': '嶋　美緒', 'nickname': 'ちあき', 'id': '1345928', 'password': 'mn15781578', 'security': '4649'},
    {'num': 10, 'name': '劉　燕林', 'nickname': 'よはん', 'id': '1350790', 'password': '0214', 'security': ''},
    {'num': 11, 'name': '森川　成美', 'nickname': 'かんだい', 'id': '1353469', 'password': 'river22', 'security': '22river'},
    {'num': 12, 'name': '菅沼　幸香', 'nickname': 'あき', 'id': '1360334', 'password': '0543', 'security': ''},
    {'num': 13, 'name': '佐藤　ひとみ', 'nickname': 'かず2', 'id': '1344403', 'password': 'hito1234', 'security': 'hito1234'},
    {'num': 14, 'name': '片桐　茉弥', 'nickname': 'げんき', 'id': '1305137', 'password': '7181', 'security': ''},
    {'num': 15, 'name': '林　剛大', 'nickname': 'たいせい', 'id': '7005179', 'password': 'Take8547', 'security': 'Take8547'},
    {'num': 16, 'name': '佐伯　毅良', 'nickname': 'さえきコーチ', 'id': '1353169', 'password': '1014', 'security': ''},
    {'num': 17, 'name': '織田　みどり', 'nickname': 'なお１', 'id': '1307199', 'password': '0516', 'security': '550516'},
    {'num': 18, 'name': '織田　千尋', 'nickname': 'なお２', 'id': '1307793', 'password': '1234', 'security': ''},
    {'num': 19, 'name': '秋葉　映舞', 'nickname': 'えま', 'id': '1377268', 'password': '0724', 'security': 'akiba724'},
    {'num': 20, 'name': '片岡　千里', 'nickname': 'はゆま', 'id': '1370075', 'password': '1983', 'security': ''},
    {'num': 21, 'name': '森川', 'nickname': 'かんだい2', 'id': '1363633', 'password': '1387', 'security': '1387'},
    {'num': 22, 'name': '島田　遼', 'nickname': 'しまだ1', 'id': '1377592', 'password': '1003', 'security': ''},
    {'num': 23, 'name': '島田　千奈美', 'nickname': 'しまだ2', 'id': '1377593', 'password': '0418', 'security': ''},
    {'num': 24, 'name': '', 'nickname': 'だいと', 'id': '1377521', 'password': '0617', 'security': ''},
    {'num': 25, 'name': '', 'nickname': 'ひろゆき2', 'id': '1383091', 'password': '5655', 'security': ''},
]

# 施設データ
FACILITIES = {
    '等々力第１サッカー場': {
        'area': '中原区',
        'group': 'サッカー場',
        'place': '等々力第１サッカー場',
        'times': ['6:00', '8:00', '10:00', '12:00', '14:00', '16:00', '18:30']
    },
    '等々力第２サッカー場': {
        'area': '中原区',
        'group': 'サッカー場',
        'place': '等々力第２サッカー場',
        'times': ['6:00', '8:00', '10:00', '12:00', '14:00', '16:00', '18:30']
    },
    '上平間サッカー場': {
        'area': '中原区',
        'group': 'サッカー場',
        'place': '上平間サッカー場',
        'times': ['6:00', '8:00', '10:00', '12:00', '14:00', '16:00', '18:00']
    },
    '丸子橋第１': {
        'area': '中原区',
        'group': '多目的広場',
        'place': '丸子橋広場',
        'facility': '丸子橋第１',
        'times': ['8:00', '12:00', '16:00']
    },
    '丸子橋第３': {
        'area': '中原区',
        'group': '多目的広場',
        'place': '丸子橋広場',
        'facility': '丸子橋第３',
        'times': ['8:00', '12:00', '16:00']
    },
    '古市場サッカー場': {
        'area': '幸区',
        'group': 'サッカー場',
        'place': '古市場サッカー場',
        'times': ['6:00', '8:00', '10:00', '12:00', '14:00', '16:00', '18:00']
    },
}

# 利用目的
PURPOSES = [
    'サッカー',
    '少年サッカー（小・中学生）',
    'ラクロス',
    'アメフト練習',
    'ラグビー練習',
]


def get_config_path():
    """設定ファイルのパスを取得"""
    if getattr(sys, 'frozen', False):
        base_path = Path(sys.executable).parent
    else:
        base_path = Path(__file__).parent
    return base_path / 'fureai_config.json'


def get_accounts_path():
    """アカウントファイルのパスを取得"""
    if getattr(sys, 'frozen', False):
        base_path = Path(sys.executable).parent
    else:
        base_path = Path(__file__).parent
    return base_path / 'fureai_accounts.json'


def load_accounts():
    """アカウントを読み込み"""
    accounts_path = get_accounts_path()
    if accounts_path.exists():
        try:
            with open(accounts_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return DEFAULT_ACCOUNTS.copy()


def save_accounts(accounts):
    """アカウントを保存"""
    accounts_path = get_accounts_path()
    with open(accounts_path, 'w', encoding='utf-8') as f:
        json.dump(accounts, f, ensure_ascii=False, indent=2)


class AccountDialog(QDialog):
    """アカウント追加/編集ダイアログ"""

    def __init__(self, parent=None, account=None):
        super().__init__(parent)
        self.setWindowTitle("アカウント追加" if account is None else "アカウント編集")
        self.setMinimumWidth(350)

        layout = QFormLayout(self)

        self.nickname_edit = QLineEdit()
        layout.addRow("ニックネーム:", self.nickname_edit)

        self.name_edit = QLineEdit()
        layout.addRow("氏名:", self.name_edit)

        self.id_edit = QLineEdit()
        layout.addRow("ユーザーID:", self.id_edit)

        self.password_edit = QLineEdit()
        layout.addRow("パスワード:", self.password_edit)

        self.security_edit = QLineEdit()
        layout.addRow("セキュリティ番号:", self.security_edit)

        # 既存アカウントの場合は値をセット
        if account:
            self.nickname_edit.setText(account.get('nickname', ''))
            self.name_edit.setText(account.get('name', ''))
            self.id_edit.setText(account.get('id', ''))
            self.password_edit.setText(account.get('password', ''))
            self.security_edit.setText(account.get('security', ''))

        # ボタン
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def get_account(self):
        """入力されたアカウント情報を取得"""
        return {
            'nickname': self.nickname_edit.text(),
            'name': self.name_edit.text(),
            'id': self.id_edit.text(),
            'password': self.password_edit.text(),
            'security': self.security_edit.text(),
        }


class ApplicationRow(QFrame):
    """1件の申込設定行"""

    def __init__(self, row_num, parent=None):
        super().__init__(parent)
        self.row_num = row_num
        self._setup_ui()

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 2, 5, 2)

        # 有効/無効チェック
        self.enabled_check = QCheckBox()
        layout.addWidget(self.enabled_check)

        # 番号
        layout.addWidget(QLabel(f"{self.row_num}"))

        # 施設選択
        self.facility_combo = QComboBox()
        self.facility_combo.addItems([''] + list(FACILITIES.keys()))
        self.facility_combo.setMinimumWidth(150)
        self.facility_combo.currentTextChanged.connect(self._on_facility_change)
        layout.addWidget(self.facility_combo)

        # 月選択
        self.month_combo = QComboBox()
        self.month_combo.addItems([''] + [str(i) for i in range(1, 13)])
        self.month_combo.setMinimumWidth(50)
        layout.addWidget(self.month_combo)
        layout.addWidget(QLabel("月"))

        # 日選択
        self.day_combo = QComboBox()
        self.day_combo.addItems([''] + [str(i) for i in range(1, 32)])
        self.day_combo.setMinimumWidth(50)
        layout.addWidget(self.day_combo)
        layout.addWidget(QLabel("日"))

        # 開始時間（デフォルトの選択肢を設定）
        self.start_time_combo = QComboBox()
        self.start_time_combo.setMinimumWidth(70)
        default_times = ['', '6:00', '8:00', '10:00', '12:00', '14:00', '16:00', '18:00', '18:30']
        self.start_time_combo.addItems(default_times)
        layout.addWidget(self.start_time_combo)

        layout.addWidget(QLabel("〜"))

        # 終了時間
        self.end_time_combo = QComboBox()
        self.end_time_combo.setMinimumWidth(70)
        default_end_times = ['', '8:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00', '20:30']
        self.end_time_combo.addItems(default_end_times)
        layout.addWidget(self.end_time_combo)

        layout.addStretch()

    def _on_facility_change(self, facility):
        """施設が変更されたら時間の選択肢を更新し、チェックを有効化"""
        self.start_time_combo.clear()
        self.end_time_combo.clear()

        if facility in FACILITIES:
            times = FACILITIES[facility]['times']
            self.start_time_combo.addItems([''] + times)
            end_times = times[1:] + (['20:30'] if '18:30' in times else ['20:00'])
            self.end_time_combo.addItems([''] + end_times)
            # 施設を選択したら自動でチェックを有効化
            self.enabled_check.setChecked(True)
        else:
            # デフォルトの選択肢
            default_times = ['', '6:00', '8:00', '10:00', '12:00', '14:00', '16:00', '18:00', '18:30']
            default_end_times = ['', '8:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00', '20:30']
            self.start_time_combo.addItems(default_times)
            self.end_time_combo.addItems(default_end_times)

    def get_data(self):
        """設定データを取得"""
        return {
            'enabled': self.enabled_check.isChecked(),
            'facility': self.facility_combo.currentText(),
            'month': self.month_combo.currentText(),
            'day': self.day_combo.currentText(),
            'start_time': self.start_time_combo.currentText(),
            'end_time': self.end_time_combo.currentText(),
        }

    def set_data(self, data):
        """設定データをセット"""
        self.enabled_check.setChecked(data.get('enabled', False))

        facility = data.get('facility', '')
        idx = self.facility_combo.findText(facility)
        if idx >= 0:
            self.facility_combo.setCurrentIndex(idx)

        month = data.get('month', '')
        idx = self.month_combo.findText(month)
        if idx >= 0:
            self.month_combo.setCurrentIndex(idx)

        day = data.get('day', '')
        idx = self.day_combo.findText(day)
        if idx >= 0:
            self.day_combo.setCurrentIndex(idx)

        start_time = data.get('start_time', '')
        idx = self.start_time_combo.findText(start_time)
        if idx >= 0:
            self.start_time_combo.setCurrentIndex(idx)

        end_time = data.get('end_time', '')
        idx = self.end_time_combo.findText(end_time)
        if idx >= 0:
            self.end_time_combo.setCurrentIndex(idx)


class FureaiApp(QMainWindow):
    """メインアプリケーション"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("ふれあいネット 抽選申込設定")
        self.setMinimumSize(900, 700)
        self.accounts = load_accounts()  # アカウントを読み込み
        self._setup_ui()
        self._load_config()

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        # === アカウント選択 ===
        account_group = QGroupBox("アカウント選択（複数選択可）")
        account_layout = QVBoxLayout(account_group)

        # 選択ボタン
        btn_layout = QHBoxLayout()
        select_all_btn = QPushButton("全選択")
        select_all_btn.clicked.connect(self._select_all_accounts)
        btn_layout.addWidget(select_all_btn)

        deselect_all_btn = QPushButton("全解除")
        deselect_all_btn.clicked.connect(self._deselect_all_accounts)
        btn_layout.addWidget(deselect_all_btn)

        btn_layout.addStretch()

        # アカウント管理ボタン
        add_account_btn = QPushButton("追加")
        add_account_btn.clicked.connect(self._add_account)
        btn_layout.addWidget(add_account_btn)

        edit_account_btn = QPushButton("編集")
        edit_account_btn.clicked.connect(self._edit_account)
        btn_layout.addWidget(edit_account_btn)

        delete_account_btn = QPushButton("削除")
        delete_account_btn.clicked.connect(self._delete_account)
        btn_layout.addWidget(delete_account_btn)

        # CSV インポート/エクスポート
        import_btn = QPushButton("CSVインポート")
        import_btn.clicked.connect(self._import_csv)
        btn_layout.addWidget(import_btn)

        export_btn = QPushButton("CSVエクスポート")
        export_btn.clicked.connect(self._export_csv)
        btn_layout.addWidget(export_btn)

        btn_layout.addStretch()

        self.selected_count_label = QLabel("選択: 0人")
        btn_layout.addWidget(self.selected_count_label)

        account_layout.addLayout(btn_layout)

        # アカウントリスト（チェックボックス付き）
        self.account_list = QListWidget()
        self.account_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.account_list.setMaximumHeight(150)

        self._refresh_account_list()

        self.account_list.itemChanged.connect(self._on_account_selection_changed)
        account_layout.addWidget(self.account_list)

        main_layout.addWidget(account_group)

        # === 共通設定 ===
        common_group = QGroupBox("共通設定")
        common_layout = QHBoxLayout(common_group)

        common_layout.addWidget(QLabel("利用目的:"))
        self.purpose_combo = QComboBox()
        self.purpose_combo.addItems(PURPOSES)
        self.purpose_combo.setCurrentIndex(1)
        common_layout.addWidget(self.purpose_combo)

        common_layout.addWidget(QLabel("人数:"))
        self.people_edit = QLineEdit("50")
        self.people_edit.setMaximumWidth(50)
        common_layout.addWidget(self.people_edit)

        common_layout.addWidget(QLabel("催し物名:"))
        self.event_edit = QLineEdit("試合")
        self.event_edit.setMaximumWidth(100)
        common_layout.addWidget(self.event_edit)

        common_layout.addStretch()
        main_layout.addWidget(common_group)

        # === 申込設定（8件） ===
        applications_group = QGroupBox("申込設定（最大8件 × 選択アカウント数）")
        applications_layout = QVBoxLayout(applications_group)

        # ヘッダー
        header = QFrame()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(5, 2, 5, 2)
        header_layout.addWidget(QLabel(""), 0)
        header_layout.addWidget(QLabel("No"), 0)
        header_layout.addWidget(QLabel("施設"), 1)
        header_layout.addWidget(QLabel("月"), 0)
        header_layout.addWidget(QLabel(""), 0)
        header_layout.addWidget(QLabel("日"), 0)
        header_layout.addWidget(QLabel(""), 0)
        header_layout.addWidget(QLabel("開始"), 0)
        header_layout.addWidget(QLabel(""), 0)
        header_layout.addWidget(QLabel("終了"), 0)
        header_layout.addStretch()
        applications_layout.addWidget(header)

        # 申込行
        self.application_rows = []
        for i in range(1, 9):
            row = ApplicationRow(i)
            applications_layout.addWidget(row)
            self.application_rows.append(row)

        applications_layout.addStretch()
        main_layout.addWidget(applications_group)

        # === 空き状況確認 ===
        availability_group = QGroupBox("空き状況")
        availability_layout = QVBoxLayout(availability_group)

        # 説明ラベル
        hint_label = QLabel("※アカウントを1つ以上選択し、申込設定を有効（チェック）にしてから確認してください")
        hint_label.setStyleSheet("color: gray; font-size: 11px;")
        availability_layout.addWidget(hint_label)

        check_btn_layout = QHBoxLayout()
        check_availability_btn = QPushButton("空き状況を確認")
        check_availability_btn.clicked.connect(self._check_availability)
        check_btn_layout.addWidget(check_availability_btn)
        check_btn_layout.addStretch()
        availability_layout.addLayout(check_btn_layout)

        # 空き状況テーブル
        self.availability_table = QTableWidget()
        self.availability_table.setColumnCount(5)
        self.availability_table.setHorizontalHeaderLabels(['施設', '日付', '時間', '空き', '申込数'])
        self.availability_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.availability_table.setMaximumHeight(150)
        availability_layout.addWidget(self.availability_table)

        main_layout.addWidget(availability_group)

        # === ボタン ===
        button_layout = QHBoxLayout()

        save_btn = QPushButton("設定を保存")
        save_btn.clicked.connect(self._save_config)
        button_layout.addWidget(save_btn)

        test_btn = QPushButton("動作確認（申込しない）")
        test_btn.clicked.connect(self._run_test)
        button_layout.addWidget(test_btn)

        real_btn = QPushButton("申込実行")
        real_btn.clicked.connect(self._run_real)
        button_layout.addWidget(real_btn)

        button_layout.addStretch()

        self.status_label = QLabel("設定を入力してください")
        button_layout.addWidget(self.status_label)

        main_layout.addLayout(button_layout)

    def _refresh_account_list(self):
        """アカウントリストを更新"""
        # 現在のチェック状態を保存
        checked_ids = set()
        for i in range(self.account_list.count()):
            item = self.account_list.item(i)
            if item.checkState() == Qt.Checked:
                acc = item.data(Qt.UserRole)
                checked_ids.add(acc['id'])

        # リストをクリアして再構築
        self.account_list.blockSignals(True)
        self.account_list.clear()

        for acc in self.accounts:
            display_name = acc['nickname']
            if acc.get('name'):
                display_name = f"{acc['nickname']}（{acc['name']}）"
            item = QListWidgetItem(display_name)
            item.setData(Qt.UserRole, acc)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Checked if acc['id'] in checked_ids else Qt.Unchecked)
            self.account_list.addItem(item)

        self.account_list.blockSignals(False)
        self._on_account_selection_changed(None)

    def _select_all_accounts(self):
        """全アカウントを選択"""
        self.account_list.blockSignals(True)
        for i in range(self.account_list.count()):
            item = self.account_list.item(i)
            item.setCheckState(Qt.Checked)
        self.account_list.blockSignals(False)
        self._on_account_selection_changed(None)

    def _deselect_all_accounts(self):
        """全アカウントの選択を解除"""
        self.account_list.blockSignals(True)
        for i in range(self.account_list.count()):
            item = self.account_list.item(i)
            item.setCheckState(Qt.Unchecked)
        self.account_list.blockSignals(False)
        self._on_account_selection_changed(None)

    def _on_account_selection_changed(self, item):
        """アカウント選択変更時"""
        count = sum(1 for i in range(self.account_list.count())
                   if self.account_list.item(i).checkState() == Qt.Checked)
        self.selected_count_label.setText(f"選択: {count}人")

    def _add_account(self):
        """アカウントを追加"""
        dialog = AccountDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            new_account = dialog.get_account()
            if not new_account['nickname'] or not new_account['id'] or not new_account['password']:
                QMessageBox.warning(self, "エラー", "ニックネーム、ユーザーID、パスワードは必須です")
                return
            # 重複チェック
            for acc in self.accounts:
                if acc['id'] == new_account['id']:
                    QMessageBox.warning(self, "エラー", "同じユーザーIDが既に存在します")
                    return
            self.accounts.append(new_account)
            save_accounts(self.accounts)
            self._refresh_account_list()
            self.status_label.setText("アカウントを追加しました")

    def _edit_account(self):
        """選択したアカウントを編集"""
        current_item = self.account_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "エラー", "編集するアカウントを選択してください")
            return

        acc = current_item.data(Qt.UserRole)
        dialog = AccountDialog(self, acc)
        if dialog.exec_() == QDialog.Accepted:
            updated_account = dialog.get_account()
            if not updated_account['nickname'] or not updated_account['id'] or not updated_account['password']:
                QMessageBox.warning(self, "エラー", "ニックネーム、ユーザーID、パスワードは必須です")
                return
            # リスト内のアカウントを更新
            for i, a in enumerate(self.accounts):
                if a['id'] == acc['id']:
                    self.accounts[i] = updated_account
                    break
            save_accounts(self.accounts)
            self._refresh_account_list()
            self.status_label.setText("アカウントを更新しました")

    def _delete_account(self):
        """選択したアカウントを削除"""
        current_item = self.account_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "エラー", "削除するアカウントを選択してください")
            return

        acc = current_item.data(Qt.UserRole)
        reply = QMessageBox.question(
            self, "確認",
            f"「{acc['nickname']}」を削除しますか？",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.accounts = [a for a in self.accounts if a['id'] != acc['id']]
            save_accounts(self.accounts)
            self._refresh_account_list()
            self.status_label.setText("アカウントを削除しました")

    def _import_csv(self):
        """CSVからアカウントをインポート（上書き）"""
        filepath, _ = QFileDialog.getOpenFileName(
            self, "CSVファイルを選択", "", "CSV Files (*.csv);;All Files (*)"
        )
        if not filepath:
            return

        try:
            new_accounts = []
            with open(filepath, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # 必須フィールドのチェック
                    if not row.get('nickname') or not row.get('id') or not row.get('password'):
                        continue
                    new_accounts.append({
                        'nickname': row.get('nickname', ''),
                        'name': row.get('name', ''),
                        'id': str(row.get('id', '')),
                        'password': str(row.get('password', '')),
                        'security': str(row.get('security', '')),
                    })

            if not new_accounts:
                QMessageBox.warning(self, "エラー", "有効なアカウントが見つかりませんでした")
                return

            reply = QMessageBox.question(
                self, "確認",
                f"{len(new_accounts)}件のアカウントをインポートします。\n"
                "現在のアカウントは上書きされます。よろしいですか？",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.accounts = new_accounts
                save_accounts(self.accounts)
                self._refresh_account_list()
                self.status_label.setText(f"{len(new_accounts)}件のアカウントをインポートしました")

        except Exception as e:
            QMessageBox.critical(self, "エラー", f"インポートに失敗しました: {e}")

    def _export_csv(self):
        """アカウントをCSVにエクスポート"""
        filepath, _ = QFileDialog.getSaveFileName(
            self, "保存先を選択", "accounts.csv", "CSV Files (*.csv);;All Files (*)"
        )
        if not filepath:
            return

        try:
            with open(filepath, 'w', encoding='utf-8-sig', newline='') as f:
                fieldnames = ['nickname', 'name', 'id', 'password', 'security']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for acc in self.accounts:
                    writer.writerow({
                        'nickname': acc.get('nickname', ''),
                        'name': acc.get('name', ''),
                        'id': acc.get('id', ''),
                        'password': acc.get('password', ''),
                        'security': acc.get('security', ''),
                    })
            self.status_label.setText(f"CSVをエクスポートしました: {filepath}")
            QMessageBox.information(self, "完了", f"{len(self.accounts)}件のアカウントをエクスポートしました")
        except Exception as e:
            QMessageBox.critical(self, "エラー", f"エクスポートに失敗しました: {e}")

    def _get_selected_accounts(self):
        """選択されたアカウントを取得"""
        selected = []
        for i in range(self.account_list.count()):
            item = self.account_list.item(i)
            if item.checkState() == Qt.Checked:
                selected.append(item.data(Qt.UserRole))
        return selected

    def _get_config(self):
        """現在の設定を取得"""
        selected_ids = [acc['id'] for acc in self._get_selected_accounts()]
        return {
            'selected_account_ids': selected_ids,
            'common': {
                'purpose': self.purpose_combo.currentText(),
                'people_num': self.people_edit.text(),
                'event_name': self.event_edit.text(),
            },
            'applications': [row.get_data() for row in self.application_rows]
        }

    def _set_config(self, config):
        """設定を反映"""
        # アカウント選択を復元
        selected_ids = config.get('selected_account_ids', [])
        for i in range(self.account_list.count()):
            item = self.account_list.item(i)
            acc = item.data(Qt.UserRole)
            if acc['id'] in selected_ids:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)

        if 'common' in config:
            idx = self.purpose_combo.findText(config['common'].get('purpose', ''))
            if idx >= 0:
                self.purpose_combo.setCurrentIndex(idx)
            self.people_edit.setText(config['common'].get('people_num', '50'))
            self.event_edit.setText(config['common'].get('event_name', '試合'))

        if 'applications' in config:
            for i, app_data in enumerate(config['applications']):
                if i < len(self.application_rows):
                    self.application_rows[i].set_data(app_data)

        self._on_account_selection_changed(None)

    def _save_config(self):
        """設定を保存"""
        config = self._get_config()
        config_path = get_config_path()

        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            self.status_label.setText("設定を保存しました")
            QMessageBox.information(self, "保存完了", "設定を保存しました")
        except Exception as e:
            QMessageBox.critical(self, "エラー", f"保存に失敗しました: {e}")

    def _load_config(self):
        """設定を読み込み"""
        config_path = get_config_path()

        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                self._set_config(config)
                self.status_label.setText("設定を読み込みました")
            except Exception as e:
                self.status_label.setText(f"設定読み込みエラー: {e}")

    def _check_availability(self):
        """空き状況を確認"""
        selected_accounts = self._get_selected_accounts()
        config = self._get_config()

        # バリデーション
        if not selected_accounts:
            QMessageBox.warning(self, "エラー", "アカウントを1つ選択してください")
            return

        enabled_apps = [app for app in config['applications'] if app['enabled']]
        if not enabled_apps:
            QMessageBox.warning(self, "エラー", "少なくとも1件の申込設定を有効にしてください")
            return

        # 最初のアカウントを使用
        acc = selected_accounts[0]

        self.status_label.setText("空き状況を確認中...")
        QApplication.processEvents()

        try:
            from fureai_auto import FureaiNet

            fureai = FureaiNet()

            if not fureai.login(acc['id'], acc['password']):
                QMessageBox.critical(self, "エラー", "ログインに失敗しました")
                self.status_label.setText("ログイン失敗")
                return

            # テーブルをクリア
            self.availability_table.setRowCount(0)

            results = []
            for app in enabled_apps:
                self.status_label.setText(f"確認中: {app['facility']} {app['month']}/{app['day']}")
                QApplication.processEvents()

                facility_data = FACILITIES.get(app['facility'], {})

                try:
                    fureai.go_to_lottery_by_area()
                    fureai.select_area(facility_data.get('area', ''))
                    fureai.select_group(facility_data.get('group', ''))
                    fureai.select_place(facility_data.get('place', ''))
                    fureai.select_facility(facility_data.get('facility', app['facility']))
                    fureai.select_date(int(app['month']), int(app['day']))

                    # 空き状況を取得
                    availability = fureai.get_availability()

                    for slot in availability['slots']:
                        results.append({
                            'facility': app['facility'],
                            'date': availability['date'],
                            'time': slot['time'],
                            'available': slot['available'],
                            'applied': slot['applied'],
                            'target_time': app['start_time'],
                        })

                except Exception as e:
                    results.append({
                        'facility': app['facility'],
                        'date': f"{app['month']}/{app['day']}",
                        'time': '-',
                        'available': 'エラー',
                        'applied': str(e)[:20],
                        'target_time': app['start_time'],
                    })

            # テーブルに結果を表示
            self.availability_table.setRowCount(len(results))
            for i, r in enumerate(results):
                self.availability_table.setItem(i, 0, QTableWidgetItem(r['facility']))
                self.availability_table.setItem(i, 1, QTableWidgetItem(r['date']))
                self.availability_table.setItem(i, 2, QTableWidgetItem(r['time']))

                # 空き状況
                avail_item = QTableWidgetItem(str(r['available']))
                if isinstance(r['available'], int):
                    if r['available'] > 0:
                        avail_item.setBackground(QColor(200, 255, 200))  # 緑（空きあり）
                    else:
                        avail_item.setBackground(QColor(255, 200, 200))  # 赤（空きなし）
                self.availability_table.setItem(i, 3, avail_item)

                self.availability_table.setItem(i, 4, QTableWidgetItem(str(r['applied'])))

                # 選択した時間帯をハイライト
                if r['time'] == r['target_time']:
                    for col in range(5):
                        item = self.availability_table.item(i, col)
                        if item:
                            font = item.font()
                            font.setBold(True)
                            item.setFont(font)

            self.status_label.setText(f"空き状況を取得しました（{len(results)}件）")

        except Exception as e:
            QMessageBox.critical(self, "エラー", f"エラー: {e}")
            self.status_label.setText(f"エラー: {e}")

    def _run_test(self):
        """テスト実行（確認画面まで）"""
        self._execute(test_mode=True)

    def _run_real(self):
        """本番実行"""
        self._execute(test_mode=False)

    def _execute(self, test_mode=True):
        """申込を実行"""
        config = self._get_config()
        selected_accounts = self._get_selected_accounts()

        # バリデーション
        if not selected_accounts:
            QMessageBox.critical(self, "エラー", "アカウントを選択してください")
            return

        enabled_apps = [app for app in config['applications'] if app['enabled']]
        if not enabled_apps:
            QMessageBox.critical(self, "エラー", "少なくとも1件の申込を有効にしてください")
            return

        # 確認
        mode_text = "動作確認（申し込みはしません）" if test_mode else "申込実行（実際に申し込みます）"
        msg = f"{mode_text}\n\n"
        msg += f"選択アカウント: {len(selected_accounts)}人\n"
        for acc in selected_accounts:
            msg += f"  - {acc['nickname']}\n"
        msg += f"\n有効な申込: {len(enabled_apps)}件\n"
        for i, app in enumerate(enabled_apps, 1):
            msg += f"  {i}. {app['facility']} {app['month']}/{app['day']} {app['start_time']}-{app['end_time']}\n"

        msg += f"\n合計: {len(selected_accounts) * len(enabled_apps)}件の申込"

        if not test_mode:
            msg += "\n\n本当に実行しますか？"

        reply = QMessageBox.question(self, "確認", msg, QMessageBox.Yes | QMessageBox.No)
        if reply != QMessageBox.Yes:
            return

        # 実行
        self.status_label.setText("実行中...")
        QApplication.processEvents()

        try:
            from fureai_auto import FureaiNet

            results = []
            total = len(selected_accounts) * len(enabled_apps)
            current = 0

            for acc in selected_accounts:
                fureai = FureaiNet()

                # ログイン
                if not fureai.login(acc['id'], acc['password']):
                    results.append(f"✗ {acc['nickname']} - ログイン失敗")
                    continue

                for app in enabled_apps:
                    current += 1
                    self.status_label.setText(f"実行中... {current}/{total}")
                    QApplication.processEvents()

                    facility_data = FACILITIES.get(app['facility'], {})

                    try:
                        fureai.go_to_lottery_by_area()
                        fureai.select_area(facility_data.get('area', ''))
                        fureai.select_group(facility_data.get('group', ''))
                        fureai.select_place(facility_data.get('place', ''))
                        fureai.select_facility(facility_data.get('facility', app['facility']))
                        fureai.select_date(int(app['month']), int(app['day']))

                        if test_mode:
                            results.append(f"✓ {acc['nickname']}: {app['facility']} {app['month']}/{app['day']} - OK")
                        else:
                            # 申込フォーム入力
                            fureai.fill_application_form(
                                start_time=app['start_time'],
                                end_time=app['end_time'],
                                purpose=config['common']['purpose'],
                                people_num=int(config['common']['people_num']),
                                event_name=config['common']['event_name']
                            )
                            # 申込実行
                            result = fureai.submit_application()
                            if result == 'success':
                                results.append(f"✓ {acc['nickname']}: {app['facility']} {app['month']}/{app['day']} - 申込完了")
                            elif result == 'error':
                                results.append(f"△ {acc['nickname']}: {app['facility']} {app['month']}/{app['day']} - スキップ（上限等）")
                            else:
                                error_detail = fureai.last_error[:100] if fureai.last_error else "不明なエラー"
                                results.append(f"✗ {acc['nickname']}: {app['facility']} {app['month']}/{app['day']} - {error_detail}")

                    except Exception as e:
                        error_detail = fureai.last_error[:100] if hasattr(fureai, 'last_error') and fureai.last_error else str(e)
                        results.append(f"✗ {acc['nickname']}: {app['facility']} {app['month']}/{app['day']} - {error_detail}")

            result_msg = "実行結果:\n\n" + "\n".join(results)
            QMessageBox.information(self, "完了", result_msg)
            self.status_label.setText("完了")

        except Exception as e:
            QMessageBox.critical(self, "エラー", f"実行エラー: {e}")
            self.status_label.setText(f"エラー: {e}")


def main():
    app = QApplication(sys.argv)
    window = FureaiApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
