export function discountTagLabel(product) {
  const discountType = normalizedDiscountType(product);
  const percent = discountPercent(product);

  if (isHalfPriceDiscount(discountType, percent)) {
    return 'Half price';
  }

  if (isHigherDiscount(discountType, percent)) {
    return percent ? `${percent}% off` : product.discount || '';
  }

  return product.discount || '';
}

export function discountTagClass(product) {
  const discountType = normalizedDiscountType(product);
  const percent = discountPercent(product);

  if (isHalfPriceDiscount(discountType, percent)) {
    return 'discount-ribbon--half';
  }

  if (isHigherDiscount(discountType, percent)) {
    return 'discount-ribbon--higher';
  }

  return '';
}

export function normalizedDiscountType(product) {
  return String(product.discount_type || product.discountType || '')
    .trim()
    .toLowerCase()
    .replace(/[\s-]+/g, '_');
}

export function discountPercent(product) {
  const explicitPercent = Number.parseFloat(String(
    product.discount_percentage ||
    product.discountPercent ||
    product.discount_percent ||
    ''
  ).replace('%', ''));

  if (Number.isFinite(explicitPercent) && explicitPercent > 0) {
    return Math.round(explicitPercent);
  }

  const price = Number(product.price);
  const priceWas = Number(product.price_was);

  if (Number.isFinite(price) && Number.isFinite(priceWas) && priceWas > price) {
    return Math.round(((priceWas - price) / priceWas) * 100);
  }

  const discountTextPercent = String(product.discount || '').match(/(\d+(?:\.\d+)?)\s*%/);
  return discountTextPercent ? Math.round(Number.parseFloat(discountTextPercent[1])) : null;
}

function isHalfPriceDiscount(discountType, percent) {
  const exactHalfTypes = ['half', 'half_price', 'halfprice', 'half_off', '50_off'];
  return exactHalfTypes.includes(discountType) || percent === 50;
}

function isHigherDiscount(discountType, percent) {
  return discountType.includes('higher') ||
    discountType.includes('greater') ||
    discountType.includes('more_than_half') ||
    discountType.includes('over_half') ||
    (Number.isFinite(percent) && percent > 50);
}
