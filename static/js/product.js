// product.js

// 获取所有"Add to Cart"按钮
const addToCartButtons = document.querySelectorAll('.add-to-cart-button');

// 获取购物车容器和关闭按钮
const shoppingCart = document.querySelector('.shopping-cart');
const closeButton = document.querySelector('.close-button');

// 针对每个"Add to Cart"按钮添加点击事件处理程序
addToCartButtons.forEach(button => {
  button.addEventListener('click', (event) => {
    // 阻止默认行为（防止按钮提交表单）
    event.preventDefault();

    // 获取所选产品的唯一标识符
    const productId = button.getAttribute('data-product');

    // 在这里执行将产品添加到购物车的逻辑（可以使用Ajax请求将产品添加到购物车）

    // 显示购物车
    shoppingCart.style.display = 'block';
  });
});

// 处理关闭按钮的点击事件
closeButton.addEventListener('click', () => {
  // 隐藏购物车
  shoppingCart.style.display = 'none';
});
