import { test, expect } from '@playwright/test';

test('登录页面可以访问', async ({ page }) => {
  const response = await page.goto('http://localhost:3000/auth/login');
  expect(response?.status()).toBe(200);
});

test('登录页面包含表单元素', async ({ page }) => {
  await page.goto('http://localhost:3000/auth/login');
  
  const emailInput = page.locator('input[type="text"]').first();
  const passwordInput = page.locator('input[type="password"]').first();
  const submitBtn = page.locator('button:has-text("登录")').first();
  
  await expect(emailInput).toBeVisible({ timeout: 10000 });
  await expect(passwordInput).toBeVisible({ timeout: 10000 });
  await expect(submitBtn).toBeVisible({ timeout: 10000 });
});

test('使用测试用户登录成功', async ({ page }) => {
  await page.goto('http://localhost:3000/auth/login');
  
  await page.fill('input[type="text"]', 'test123@example.com');
  await page.fill('input[type="password"]', '123456');
  
  const loginBtn = page.locator('button:has-text("登录")').first();
  await loginBtn.click();
  
  await page.waitForTimeout(5000);
  
  const url = page.url();
  console.log('当前URL:', url);
  
  if (url.includes('portfolio')) {
    console.log('登录成功，已跳转到投资组合页面');
  } else {
    const errorMsg = await page.locator('.el-message--error, .el-alert__title, .error-message').first().textContent().catch(() => '无错误信息');
    console.log('错误信息:', errorMsg);
  }
  
  expect(url).toContain('portfolio');
});

test('登录后可以看到导航菜单', async ({ page }) => {
  await page.goto('http://localhost:3000/auth/login');
  
  await page.fill('input[type="text"]', 'test123@example.com');
  await page.fill('input[type="password"]', '123456');
  await page.locator('button:has-text("登录")').first().click();
  
  await page.waitForTimeout(5000);
  
  const url = page.url();
  if (!url.includes('portfolio')) {
    test.skip();
  }
  
  await expect(page.locator('text=投资组合').first()).toBeVisible({ timeout: 10000 });
  await expect(page.locator('text=资产管理').first()).toBeVisible({ timeout: 10000 });
});

test('可以访问资产管理页面', async ({ page }) => {
  await page.goto('http://localhost:3000/auth/login');
  
  await page.fill('input[type="text"]', 'test123@example.com');
  await page.fill('input[type="password"]', '123456');
  await page.locator('button:has-text("登录")').first().click();
  
  await page.waitForTimeout(5000);
  
  const url = page.url();
  if (!url.includes('portfolio')) {
    test.skip();
  }
  
  await page.click('text=资产管理');
  await page.waitForTimeout(2000);
  
  expect(page.url()).toContain('/asset');
});

test('可以访问市场数据页面', async ({ page }) => {
  await page.goto('http://localhost:3000/auth/login');
  
  await page.fill('input[type="text"]', 'test123@example.com');
  await page.fill('input[type="password"]', '123456');
  await page.locator('button:has-text("登录")').first().click();
  
  await page.waitForTimeout(5000);
  
  const url = page.url();
  if (!url.includes('portfolio')) {
    test.skip();
  }
  
  await page.click('text=市场数据');
  await page.waitForTimeout(2000);
  
  expect(page.url()).toContain('/market');
});

test('可以访问业绩分析页面', async ({ page }) => {
  await page.goto('http://localhost:3000/auth/login');
  
  await page.fill('input[type="text"]', 'test123@example.com');
  await page.fill('input[type="password"]', '123456');
  await page.locator('button:has-text("登录")').first().click();
  
  await page.waitForTimeout(5000);
  
  const url = page.url();
  if (!url.includes('portfolio')) {
    test.skip();
  }
  
  await page.click('text=业绩分析');
  await page.waitForTimeout(2000);
  
  expect(page.url()).toContain('/performance');
});

test('可以访问现金管理页面', async ({ page }) => {
  await page.goto('http://localhost:3000/auth/login');
  
  await page.fill('input[type="text"]', 'test123@example.com');
  await page.fill('input[type="password"]', '123456');
  await page.locator('button:has-text("登录")').first().click();
  
  await page.waitForTimeout(5000);
  
  const url = page.url();
  if (!url.includes('portfolio')) {
    test.skip();
  }
  
  await page.click('text=现金管理');
  await page.waitForTimeout(2000);
  
  expect(page.url()).toContain('/cash');
});

test('可以访问报告页面', async ({ page }) => {
  await page.goto('http://localhost:3000/auth/login');
  
  await page.fill('input[type="text"]', 'test123@example.com');
  await page.fill('input[type="password"]', '123456');
  await page.locator('button:has-text("登录")').first().click();
  
  await page.waitForTimeout(5000);
  
  const url = page.url();
  if (!url.includes('portfolio')) {
    test.skip();
  }
  
  await page.click('text=报告');
  await page.waitForTimeout(2000);
  
  expect(page.url()).toContain('/report');
});

test('可以新增投资组合', async ({ page }) => {
  // 登录
  await page.goto('http://localhost:3000/auth/login');
  await page.fill('input[type="text"]', 'test123@example.com');
  await page.fill('input[type="password"]', '123456');
  await page.locator('button:has-text("登录")').first().click();
  await page.waitForTimeout(3000);
  
  // 确保登录成功
  const urlAfterLogin = page.url();
  if (!urlAfterLogin.includes('portfolio')) {
    test.skip();
  }
  
  // 点击创建投资组合按钮
  const createBtn = page.locator('button:has-text("创建"), a:has-text("创建"), button:has-text("新增")').first();
  await createBtn.click();
  await page.waitForTimeout(1000);
  
  // 确认进入创建页面
  expect(page.url()).toContain('/portfolio/create');
  
  // 填写表单
  const uniqueName = `测试组合_${Date.now()}`;
  await page.fill('input[placeholder="请输入组合名称"]', uniqueName);
  await page.fill('textarea[placeholder="请输入组合描述"]', '这是一个自动化测试创建的投资组合');
  
  // 选择业绩基准
  await page.click('.el-select:has-text("请选择业绩基准")');
  await page.waitForTimeout(500);
  await page.click('.el-select-dropdown__item:has-text("沪深300")');
  
  // 选择风险等级
  await page.click('.el-select:has-text("请选择风险等级")');
  await page.waitForTimeout(500);
  await page.click('.el-select-dropdown__item:has-text("中风险")');
  
  // 点击创建按钮
  await page.click('button:has-text("创建")');
  await page.waitForTimeout(3000);
  
  // 验证跳转回投资组合列表页
  const finalUrl = page.url();
  expect(finalUrl).toContain('/portfolio');
  expect(finalUrl).not.toContain('/create');
  
  // 验证新创建的组合出现在列表中
  await expect(page.locator(`text=${uniqueName}`)).toBeVisible({ timeout: 5000 });
  
  console.log(`投资组合 "${uniqueName}" 创建成功`);
});

test('可以添加投资组合持仓', async ({ page }) => {
  // 登录
  await page.goto('http://localhost:3000/auth/login');
  await page.fill('input[type="text"]', 'test123@example.com');
  await page.fill('input[type="password"]', '123456');
  await page.locator('button:has-text("登录")').first().click();
  await page.waitForTimeout(3000);
  
  // 确保登录成功
  const urlAfterLogin = page.url();
  if (!urlAfterLogin.includes('portfolio')) {
    test.skip();
  }
  
  // 等待投资组合列表加载
  await page.waitForTimeout(2000);
  
  // 点击第一个投资组合的"查看"按钮进入详情页
  const viewBtn = page.locator('button:has-text("查看")').first();
  await viewBtn.click();
  await page.waitForTimeout(2000);
  
  // 确认进入投资组合详情页
  const detailUrl = page.url();
  expect(detailUrl).toContain('/portfolio/');
  expect(detailUrl).not.toContain('/create');
  console.log('进入投资组合详情页:', detailUrl);
  
  // 点击添加持仓按钮
  const addHoldingBtn = page.locator('button:has-text("添加持仓")').first();
  await addHoldingBtn.click();
  await page.waitForTimeout(1000);
  
  // 确认对话框打开
  const dialog = page.locator('.el-dialog:visible');
  await expect(dialog).toBeVisible({ timeout: 5000 });
  console.log('对话框已打开');
  
  // 选择资产 - 点击下拉框
  const assetSelect = dialog.locator('.el-select').first();
  await assetSelect.click();
  await page.waitForTimeout(500);
  
  // 选择第一个资产选项
  const firstAsset = page.locator('.el-select-dropdown__item').first();
  await firstAsset.click();
  await page.waitForTimeout(500);
  console.log('已选择资产');
  
  // 填写持仓数量 - 使用 el-input-number 的 input
  const quantityInput = dialog.locator('.el-input-number input').first();
  await quantityInput.click();
  await quantityInput.fill('1000');
  await page.waitForTimeout(300);
  
  // 填写成本价
  const costPriceInput = dialog.locator('.el-input-number input').nth(1);
  await costPriceInput.click();
  await costPriceInput.fill('10.50');
  await page.waitForTimeout(300);
  
  // 填写当前价（如果有）
  const currentPriceInput = dialog.locator('.el-input-number input').nth(2);
  if (await currentPriceInput.count() > 0) {
    await currentPriceInput.click();
    await currentPriceInput.fill('12.00');
  }
  console.log('已填写持仓信息');
  
  // 点击确定按钮
  const confirmBtn = dialog.locator('button:has-text("确定")');
  await confirmBtn.click();
  await page.waitForTimeout(3000);
  
  // 验证成功提示
  const successMessage = page.locator('.el-message--success');
  await expect(successMessage).toBeVisible({ timeout: 5000 });
  console.log('持仓添加成功');

  // 验证持仓明细列表中包含刚添加的持仓
  await page.waitForTimeout(2000);

  // 检查表格中是否有数据行
  const tableBody = page.locator('.el-table__body-wrapper tbody');
  await expect(tableBody).toBeVisible({ timeout: 5000 });

  // 检查表格行数
  const tableRows = page.locator('.el-table__body-wrapper tbody tr');
  const rowCount = await tableRows.count();
  expect(rowCount).toBeGreaterThan(0);
  console.log(`持仓列表共有 ${rowCount} 行`);

  // 验证持仓数量是否正确显示
  const quantityCell = page.locator('.el-table__body-wrapper tbody td').filter({ hasText: '1000' }).first();
  await expect(quantityCell).toBeVisible({ timeout: 5000 });
  console.log('持仓列表中包含数量为 1000 的持仓');

  // 验证成本价是否正确显示
  const costPriceCell = page.locator('.el-table__body-wrapper tbody td').filter({ hasText: '10.5' }).first();
  await expect(costPriceCell).toBeVisible({ timeout: 5000 });
  console.log('持仓列表中包含成本价为 10.5 的持仓');

  // 验证当前价是否正确显示
  const currentPriceCell = page.locator('.el-table__body-wrapper tbody td').filter({ hasText: '12' }).first();
  await expect(currentPriceCell).toBeVisible({ timeout: 5000 });
  console.log('持仓列表中包含当前价为 12 的持仓');

  console.log('持仓明细列表验证通过');
});
