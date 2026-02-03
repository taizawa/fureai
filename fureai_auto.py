#!/usr/bin/env python3
"""
川崎市ふれあいネット自動申込プログラム
https://www.fureai-net.city.kawasaki.jp/sp/
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

BASE_URL = "https://www.fureai-net.city.kawasaki.jp/sp/"


class FureaiNet:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15'
        })
        self.current_url = BASE_URL
        self.last_error = ""  # エラー詳細を保存
        self._user_id = None  # 再ログイン用
        self._password = None

    def _set_error(self, message):
        """エラー情報を設定"""
        page_text = self.soup.get_text()[:500] if hasattr(self, 'soup') and self.soup else ""
        self.last_error = f"{message}\n\nURL: {self.current_url}\n\nページ内容:\n{page_text}"
        print(f"  → {message}")
        print(f"  → URL: {self.current_url}")

    def _get_soup(self, response):
        """レスポンスをBeautifulSoupでパース"""
        response.encoding = 'shift_jis'
        self.current_url = response.url
        return BeautifulSoup(response.text, 'html.parser')

    def _get_hidden_fields(self, soup):
        """隠しフィールドを取得"""
        return {
            inp.get('name'): inp.get('value', '')
            for inp in soup.find_all('input', type='hidden')
            if inp.get('name')
        }

    def _submit_form(self, soup, extra_data=None):
        """フォームを送信"""
        form = soup.find('form')
        if not form:
            return None

        action = urljoin(self.current_url, form.get('action', ''))
        data = {}

        for inp in form.find_all('input'):
            name = inp.get('name')
            if name:
                data[name] = inp.get('value', '')

        for select in form.find_all('select'):
            name = select.get('name')
            if name:
                selected = select.find('option', selected=True)
                data[name] = selected.get('value', '') if selected else ''

        if extra_data:
            data.update(extra_data)

        return self.session.post(action, data=data)

    def _click_link(self, soup, text_pattern):
        """テキストを含むリンクをクリック"""
        for a in soup.find_all('a'):
            link_text = a.get_text(strip=True)
            if text_pattern in link_text:
                href = a.get('href', '')
                if href:
                    url = urljoin(self.current_url, href)
                    print(f"  → クリック: {link_text}")
                    return self.session.get(url)
        return None

    def _click_link_by_index(self, soup, list_selector, index):
        """リスト内のn番目のリンクをクリック"""
        links = soup.select(list_selector + ' a')
        if index <= len(links):
            a = links[index - 1]
            href = a.get('href', '')
            text = a.get_text(strip=True)
            if href:
                url = urljoin(self.current_url, href)
                print(f"  → クリック: {text}")
                return self.session.get(url)
        return None

    def login(self, user_id: str, password: str) -> bool:
        """ログイン"""
        print("[1] ログイン")

        # 再ログイン用に保存
        self._user_id = user_id
        self._password = password

        response = self.session.get(BASE_URL)
        soup = self._get_soup(response)

        hidden = self._get_hidden_fields(soup)
        form = soup.find('form')
        action_url = urljoin(BASE_URL, form.get('action', ''))

        response = self.session.post(action_url, data={
            'userId': user_id,
            'password': password,
            'securityNo': '',
            'login': '認証',
            **hidden
        })
        soup = self._get_soup(response)

        if 'エラー' in soup.get_text():
            print("  → ログイン失敗")
            return False

        print(f"  → ログイン成功")

        # 次へボタン
        response = self._submit_form(soup)
        self.soup = self._get_soup(response)
        return True

    def go_to_lottery_by_area(self):
        """抽選申し込み → 地域から"""
        print("[2] 抽選申し込み → 地域から")

        # 直接「地域から」のURLにアクセス
        url = urljoin(BASE_URL, '/sp/lotPTransLotAcceptAreaAction.do?displayNo=papae1000&lotSetupItem=3')
        response = self.session.get(url)
        self.soup = self._get_soup(response)

        # エラー画面（セッション切れ等）を検出したら再ログイン
        if 'エラー' in self.soup.get_text() or '認証' in self.soup.get_text():
            print("  → セッション切れ、再ログイン中...")
            if self._user_id and self._password:
                self.login(self._user_id, self._password)
                # 再度地域選択画面にアクセス
                response = self.session.get(url)
                self.soup = self._get_soup(response)

        print("  → 地域選択画面へ移動")
        return True

    def select_area(self, area_name: str):
        """地域を選択"""
        print(f"[3] 地域選択: {area_name}")
        response = self._click_link(self.soup, area_name)
        if not response:
            self._set_error(f"{area_name}が見つかりません")
            return False
        self.soup = self._get_soup(response)
        return True

    def select_group(self, group_name: str):
        """グループを選択"""
        print(f"[4] グループ選択: {group_name}")
        response = self._click_link(self.soup, group_name)
        if not response:
            self._set_error(f"{group_name}が見つかりません")
            return False
        self.soup = self._get_soup(response)
        return True

    def select_place(self, place_name: str):
        """館を選択"""
        print(f"[5] 館選択: {place_name}")
        response = self._click_link(self.soup, place_name)
        if not response:
            self._set_error(f"{place_name}が見つかりません")
            return False
        self.soup = self._get_soup(response)
        return True

    def select_facility(self, facility_name: str):
        """施設を選択"""
        print(f"[6] 施設選択: {facility_name}")
        response = self._click_link(self.soup, facility_name)
        if not response:
            self._set_error(f"{facility_name}が見つかりません")
            return False
        self.soup = self._get_soup(response)
        return True

    def select_date(self, month: int, day: int):
        """日付を選択"""
        print(f"[7] 日付選択: {month}月{day}日")

        form = self.soup.find('form')
        if not form:
            self._set_error("日付選択フォームが見つかりません")
            return False

        action = urljoin(self.current_url, form.get('action', ''))
        hidden = self._get_hidden_fields(self.soup)

        # 月、日、決定ボタンを1回で送信
        data = {
            'selectMonth': str(month),
            'selectDay': str(day),
            **hidden
        }

        response = self.session.post(action, data=data)
        self.soup = self._get_soup(response)
        return True

    def fill_application_form(self, start_time: str, end_time: str,
                               purpose: str = "少年サッカー（小・中学生）",
                               people_num: int = 50,
                               event_name: str = "試合"):
        """申込フォームを入力して確認画面まで進む"""
        print(f"[8] 申込フォーム入力")
        print(f"  → 時間: {start_time} - {end_time}")
        print(f"  → 目的: {purpose}")
        print(f"  → 人数: {people_num}")
        print(f"  → イベント: {event_name}")

        # フォーム構造を確認
        form = self.soup.find('form')
        if not form:
            self._set_error("申込フォームが見つかりません")
            return False

        action = urljoin(self.current_url, form.get('action', ''))
        hidden = self._get_hidden_fields(self.soup)

        # selectの選択肢を確認してvalue取得
        stime_value = start_time
        etime_value = end_time
        purpose_value = None

        for select in self.soup.find_all('select'):
            name = select.get('name', '')
            if name == 'selectStime':
                for opt in select.find_all('option'):
                    if start_time in opt.get_text():
                        stime_value = opt.get('value', start_time)
            elif name == 'selectEtime':
                for opt in select.find_all('option'):
                    if end_time in opt.get_text():
                        etime_value = opt.get('value', end_time)
            elif name == 'appliedPpsCd':
                for opt in select.find_all('option'):
                    if purpose in opt.get_text():
                        purpose_value = opt.get('value')

        print(f"  → 時間値: {stime_value} - {etime_value}")
        print(f"  → 目的値: {purpose_value}")

        # フォームデータを構築
        data = {
            'selectStime': stime_value,
            'selectEtime': etime_value,
            'appliedPpsCd': purpose_value or '',
            'appliedPeopleNum': str(people_num),
            'eventName': event_name,
            'groupName': '',
            **hidden
        }

        # Shift-JISでエンコードして送信
        encoded_data = {k: v.encode('shift_jis') if isinstance(v, str) else v for k, v in data.items()}
        response = self.session.post(action, data=encoded_data)
        self.soup = self._get_soup(response)

        # エラーチェック（空きがない場合など）
        page_text = self.soup.get_text()
        if 'エラー' in page_text:
            error_msg = "確認画面でエラー"
            if '空きがありません' in page_text:
                error_msg = "空きがありません（当選可能数が0）"
            self._set_error(error_msg)
            # エラー後にTOPに戻る（次の申し込みのため）
            self._go_to_top()
            return False

        print("  → 確認画面へ進みました")
        return True

    def submit_application(self):
        """申し込みを実行

        Returns:
            'success': 申し込み成功
            'error': スキップ可能なエラー（上限到達など）
            'fatal': 致命的なエラー（フォームが見つからないなど）
        """
        print("[9] 申し込み実行")

        form = self.soup.find('form')
        if not form:
            self._set_error("申込実行フォームが見つかりません")
            return 'fatal'

        action = urljoin(self.current_url, form.get('action', ''))
        hidden = self._get_hidden_fields(self.soup)

        # 申し込みボタンを探す
        submit_btn = None
        for inp in form.find_all('input', type='submit'):
            value = inp.get('value', '')
            if '申込' in value or '確定' in value or '登録' in value or '決定' in value:
                submit_btn = inp
                break

        if not submit_btn:
            # submitボタンがなければ、通常のボタンを探す
            for btn in form.find_all('button'):
                text = btn.get_text(strip=True)
                if '申込' in text or '確定' in text or '登録' in text or '決定' in text:
                    submit_btn = btn
                    break

        data = {**hidden}
        if submit_btn and submit_btn.get('name') and submit_btn.get('name') != 'None':
            data[submit_btn.get('name')] = submit_btn.get('value', '')

        # 申し込みを送信
        response = self.session.post(action, data=data)
        self.soup = self._get_soup(response)

        # 結果を確認
        page_text = self.soup.get_text()
        if 'エラー' in page_text:
            print("  → 申し込みエラー（スキップ）")
            # エラー内容を簡潔に表示
            error_lines = [line.strip() for line in page_text.split('\n') if 'エラー' in line or '上限' in line or '件数' in line]
            if error_lines:
                for line in error_lines[:3]:
                    print(f"    {line}")
            return 'error'

        print("  → 申し込み完了")

        # メール送信確認画面を処理（連続申し込みのため）
        self._handle_mail_confirmation()

        return 'success'

    def _handle_mail_confirmation(self):
        """メール送信確認画面を処理してTOPに戻る"""
        page_text = self.soup.get_text()
        if 'メール送信確認' not in page_text:
            return

        # 「はい」を押してメール送信
        form = self.soup.find('form')
        if form:
            action = urljoin(self.current_url, form.get('action', ''))
            hidden = self._get_hidden_fields(self.soup)
            response = self.session.post(action, data=hidden)
            self.soup = self._get_soup(response)

        # 「TOP画面へ」をクリックしてメインメニューに戻る
        response = self._click_link(self.soup, 'TOP画面へ')
        if response:
            self.soup = self._get_soup(response)

    def _go_to_top(self):
        """メインメニュー（TOP画面）に戻る"""
        # 直接メインメニューURLにアクセス（「もどる」は別画面に戻ることがあるため）
        url = urljoin(BASE_URL, '/sp/rsvPTransMainMenuAction.do')
        response = self.session.get(url)
        self.soup = self._get_soup(response)

    def get_availability(self):
        """現在の画面から空き状況を取得"""
        result = {
            'date': '',
            'slots': []  # [{'time': '6:00', 'available': 1, 'applied': 0}, ...]
        }

        import re

        # 日付を抽出（例: 2026年3月9日）
        page_text = self.soup.get_text()
        date_match = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日', page_text)
        if date_match:
            result['date'] = f"{date_match.group(1)}年{date_match.group(2)}月{date_match.group(3)}日"

        # 申込状況のdivを探す
        # HTMLの構造: <div class="ws-normal fw-normal">...<br/>０６００ 0<br/>０８００ 1/2<br/>...</div>
        status_div = self.soup.find('div', class_='ws-normal fw-normal')
        if not status_div:
            return result

        # HTMLを取得して<br>で分割
        html_content = str(status_div)
        # <br/>や<br>で分割
        lines = re.split(r'<br\s*/?>', html_content)

        # 全角数字を半角に変換
        def zen_to_han(text):
            return text.translate(str.maketrans('０１２３４５６７８９', '0123456789'))

        # 時間コードと表示時間のマッピング
        time_map = {
            '0600': '6:00',
            '0800': '8:00',
            '1000': '10:00',
            '1200': '12:00',
            '1400': '14:00',
            '1600': '16:00',
            '1800': '18:00',
            '1830': '18:30',
        }

        for line in lines:
            # タグを除去
            line_clean = re.sub(r'<[^>]+>', '', line).strip()
            line_han = zen_to_han(line_clean)

            # パターン: "0600 0" or "0800 1/2"
            match = re.match(r'(\d{4})\s+(\d+(?:/\d+)?)', line_han)
            if match:
                time_code = match.group(1)
                value = match.group(2)

                time_label = time_map.get(time_code, time_code)

                if '/' in value:
                    parts = value.split('/')
                    available = int(parts[0])
                    applied = int(parts[1])
                else:
                    available = int(value) if value != '0' else 0
                    applied = 0

                result['slots'].append({
                    'time': time_label,
                    'available': available,
                    'applied': applied,
                })

        return result

    def show_current_page(self):
        """現在のページを表示"""
        print()
        print("--- 現在のページ ---")
        print(self.soup.get_text()[:1000])


def main():
    # アカウント情報
    USER_ID = "1357703"
    PASSWORD = "1983"

    # 予約情報
    FACILITY = {
        'area': '中原区',
        'group': 'サッカー場',
        'place': '等々力第１サッカー場',  # 全角１
        'facility': '等々力第１サッカー場',
    }
    DATE = {'month': 3, 'day': 9}
    TIME = {'start': '10:00', 'end': '12:00'}

    print("=" * 50)
    print("川崎市ふれあいネット 自動入力プログラム")
    print("=" * 50)
    print(f"施設: {FACILITY['facility']}")
    print(f"日時: {DATE['month']}月{DATE['day']}日 {TIME['start']}-{TIME['end']}")
    print("=" * 50)
    print()

    fureai = FureaiNet()

    # 1. ログイン
    if not fureai.login(USER_ID, PASSWORD):
        return

    # 2. 抽選申し込み → 地域から
    if not fureai.go_to_lottery_by_area():
        fureai.show_current_page()
        return

    # 3. 地域選択
    if not fureai.select_area(FACILITY['area']):
        fureai.show_current_page()
        return

    # 4. グループ選択
    if not fureai.select_group(FACILITY['group']):
        fureai.show_current_page()
        return

    # 5. 館選択
    if not fureai.select_place(FACILITY['place']):
        fureai.show_current_page()
        return

    # 6. 施設選択
    if not fureai.select_facility(FACILITY['facility']):
        fureai.show_current_page()
        return

    # 7. 日付選択
    if not fureai.select_date(DATE['month'], DATE['day']):
        fureai.show_current_page()
        return

    # 8. 時間・目的・人数を入力
    if not fureai.fill_application_form(
        start_time=TIME['start'],
        end_time=TIME['end'],
        purpose='少年サッカー（小・中学生）',
        people_num=50,
        event_name='試合'
    ):
        fureai.show_current_page()
        return

    # 9. 申し込み実行
    result = fureai.submit_application()
    if result == 'fatal':
        fureai.show_current_page()
        return
    elif result == 'error':
        print("  → エラーのためこの申し込みはスキップしました")

    print()
    print("=" * 50)
    print("申し込み処理が完了しました")
    print("=" * 50)


if __name__ == "__main__":
    main()
