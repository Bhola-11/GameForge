from typing import Dict, Any
from decimal import Decimal

class StorefrontCatalogService:
    @staticmethod
    def calculate_localized_regional_pricing(base_price_usd: Decimal, region_code: str) -> Dict[str, Any]:
        multipliers = {
            'US': {'currency': 'USD', 'multiplier': Decimal('1.0')},
            'EU': {'currency': 'EUR', 'multiplier': Decimal('0.92')},
            'GB': {'currency': 'GBP', 'multiplier': Decimal('0.79')},
            'JP': {'currency': 'JPY', 'multiplier': Decimal('155.0')},
            'BR': {'currency': 'BRL', 'multiplier': Decimal('3.5')},
        }
        config = multipliers.get(region_code, multipliers['US'])
        converted_price = base_price_usd * config['multiplier']
        
        return {
            "region": region_code,
            "currency": config['currency'],
            "price": round(converted_price, 2) if config['currency'] != 'JPY' else round(converted_price, 0),
            "base_usd": float(base_price_usd)
        }
