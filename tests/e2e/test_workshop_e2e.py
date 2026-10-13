import re
from playwright.sync_api import expect
def test_user_creates_car_in_browser(page, live_server):
    page.goto(f"{live_server}/cars/new")

    page.get_by_label("Make", exact=True).fill("Toyota")
    page.get_by_label("Model", exact=True).fill("Yaris")
    page.get_by_label("Year", exact=True).fill("2020")
    page.get_by_label("Color", exact=False).fill("Blue")
    page.get_by_role("button", name="Create").click()
    expect(page).to_have_url(re.compile(r"/cars/\d+$"))
    expect(page.get_by_role("heading", name="Toyota Yaris")).to_be_visible()
def test_user_edits_car_and_change_survives_reload(page, live_server):
    page.goto(f"{live_server}/cars/new")
    # 创建 Honda Civic
    page.get_by_label("Make", exact=True).fill("Honda")
    page.get_by_label("Model", exact=True).fill("Civic")
    page.get_by_label("Year", exact=True).fill("2022")
    page.get_by_label("Color", exact=False).fill("Blue")
    page.get_by_role("button", name="Create").click()
    
    # 等待跳转到详情页
    expect(page).to_have_url(re.compile(r"/cars/\d+$"))
    
    # 点击 Edit car 链接
    page.get_by_role("link", name="Edit car").click()
    
    # 修改型号和年份（使用更稳健的属性选择器确保能定位到输入框）
    page.locator("input[name='model'], #model").fill("Accord")
    page.locator("input[name='year'], #year").fill("2023")
    
    # 点击表单的提交按钮，并等待页面跳转回详情页
    with page.expect_navigation():
        page.locator("button[type='submit'], input[type='submit']").click()
    
    # 断言详情页标题为 Honda Accord
    expect(page.get_by_role("heading", name="Honda Accord")).to_be_visible()
    
    # 刷新页面
    page.reload()
    
    # 断言更改仍然存在
    expect(page.locator("#car-model")).to_have_text("Accord")
    expect(page.locator("#car-year")).to_have_text("2023")
