/**
 * 国际区号数据
 * 包含全球主要国家的区号信息和校验规则
 */

export const countryCodes = [
  {
    code: 'CN',
    name: '中国',
    nameEn: 'China',
    dialCode: '+86',
    flag: 'CN',
    minLength: 11,
    maxLength: 11,
    pattern: /^1[3-9]\d{9}$/,
    placeholder: '138 1234 5678',
    validate: (digits) => {
      // 以1开头，第二位为3-9，总长度11位
      return /^1[3-9]\d{9}$/.test(digits)
    }
  },
  {
    code: 'US',
    name: '美国',
    nameEn: 'United States',
    dialCode: '+1',
    flag: 'US',
    minLength: 10,
    maxLength: 10,
    pattern: /^\d{10}$/,
    placeholder: '123 456 7890',
    validate: (digits) => {
      // 10位数字
      return /^\d{10}$/.test(digits)
    }
  },
  {
    code: 'GB',
    name: '英国',
    nameEn: 'United Kingdom',
    dialCode: '+44',
    flag: 'GB',
    minLength: 10,
    maxLength: 11,
    pattern: /^\d{10,11}$/,
    placeholder: '7123 456789',
    validate: (digits) => {
      // 允许11位（以0开头）或10位（去掉前导0）
      if (digits.length === 11 && digits.startsWith('0')) {
        return /^\d{11}$/.test(digits)
      }
      return /^\d{10}$/.test(digits)
    }
  },
  {
    code: 'JP',
    name: '日本',
    nameEn: 'Japan',
    dialCode: '+81',
    flag: 'JP',
    minLength: 10,
    maxLength: 11,
    pattern: /^\d{10,11}$/,
    placeholder: '90 1234 5678',
    validate: (digits) => {
      return /^\d{10,11}$/.test(digits)
    }
  },
  {
    code: 'KR',
    name: '韩国',
    nameEn: 'South Korea',
    dialCode: '+82',
    flag: 'KR',
    minLength: 10,
    maxLength: 11,
    pattern: /^\d{10,11}$/,
    placeholder: '10 1234 5678',
    validate: (digits) => {
      return /^\d{10,11}$/.test(digits)
    }
  },
  {
    code: 'HK',
    name: '中国香港',
    nameEn: 'Hong Kong',
    dialCode: '+852',
    flag: 'HK',
    minLength: 8,
    maxLength: 8,
    pattern: /^\d{8}$/,
    placeholder: '9123 4567',
    validate: (digits) => {
      return /^\d{8}$/.test(digits)
    }
  },
  {
    code: 'TW',
    name: '中国台湾',
    nameEn: 'Taiwan',
    dialCode: '+886',
    flag: 'TW',
    minLength: 9,
    maxLength: 9,
    pattern: /^\d{9}$/,
    placeholder: '912 345 678',
    validate: (digits) => {
      return /^\d{9}$/.test(digits)
    }
  },
  {
    code: 'MO',
    name: '中国澳门',
    nameEn: 'Macau',
    dialCode: '+853',
    flag: 'MO',
    minLength: 8,
    maxLength: 8,
    pattern: /^\d{8}$/,
    placeholder: '6123 4567',
    validate: (digits) => {
      return /^\d{8}$/.test(digits)
    }
  },
  {
    code: 'SG',
    name: '新加坡',
    nameEn: 'Singapore',
    dialCode: '+65',
    flag: 'SG',
    minLength: 8,
    maxLength: 8,
    pattern: /^\d{8}$/,
    placeholder: '8123 4567',
    validate: (digits) => {
      return /^\d{8}$/.test(digits)
    }
  },
  {
    code: 'MY',
    name: '马来西亚',
    nameEn: 'Malaysia',
    dialCode: '+60',
    flag: 'MY',
    minLength: 9,
    maxLength: 10,
    pattern: /^\d{9,10}$/,
    placeholder: '12 345 6789',
    validate: (digits) => {
      return /^\d{9,10}$/.test(digits)
    }
  },
  {
    code: 'TH',
    name: '泰国',
    nameEn: 'Thailand',
    dialCode: '+66',
    flag: 'TH',
    minLength: 9,
    maxLength: 9,
    pattern: /^\d{9}$/,
    placeholder: '81 234 5678',
    validate: (digits) => {
      return /^\d{9}$/.test(digits)
    }
  },
  {
    code: 'VN',
    name: '越南',
    nameEn: 'Vietnam',
    dialCode: '+84',
    flag: 'VN',
    minLength: 9,
    maxLength: 10,
    pattern: /^\d{9,10}$/,
    placeholder: '91 234 5678',
    validate: (digits) => {
      return /^\d{9,10}$/.test(digits)
    }
  },
  {
    code: 'PH',
    name: '菲律宾',
    nameEn: 'Philippines',
    dialCode: '+63',
    flag: 'PH',
    minLength: 10,
    maxLength: 10,
    pattern: /^\d{10}$/,
    placeholder: '912 345 6789',
    validate: (digits) => {
      return /^\d{10}$/.test(digits)
    }
  },
  {
    code: 'ID',
    name: '印度尼西亚',
    nameEn: 'Indonesia',
    dialCode: '+62',
    flag: 'ID',
    minLength: 10,
    maxLength: 12,
    pattern: /^\d{10,12}$/,
    placeholder: '812 3456 7890',
    validate: (digits) => {
      return /^\d{10,12}$/.test(digits)
    }
  },
  {
    code: 'IN',
    name: '印度',
    nameEn: 'India',
    dialCode: '+91',
    flag: 'IN',
    minLength: 10,
    maxLength: 10,
    pattern: /^\d{10}$/,
    placeholder: '98765 43210',
    validate: (digits) => {
      return /^\d{10}$/.test(digits)
    }
  },
  {
    code: 'AU',
    name: '澳大利亚',
    nameEn: 'Australia',
    dialCode: '+61',
    flag: 'AU',
    minLength: 9,
    maxLength: 9,
    pattern: /^\d{9}$/,
    placeholder: '412 345 678',
    validate: (digits) => {
      return /^\d{9}$/.test(digits)
    }
  },
  {
    code: 'CA',
    name: '加拿大',
    nameEn: 'Canada',
    dialCode: '+1',
    flag: 'CA',
    minLength: 10,
    maxLength: 10,
    pattern: /^\d{10}$/,
    placeholder: '416 123 4567',
    validate: (digits) => {
      return /^\d{10}$/.test(digits)
    }
  },
  {
    code: 'DE',
    name: '德国',
    nameEn: 'Germany',
    dialCode: '+49',
    flag: 'DE',
    minLength: 10,
    maxLength: 11,
    pattern: /^\d{10,11}$/,
    placeholder: '151 12345678',
    validate: (digits) => {
      return /^\d{10,11}$/.test(digits)
    }
  },
  {
    code: 'FR',
    name: '法国',
    nameEn: 'France',
    dialCode: '+33',
    flag: 'FR',
    minLength: 9,
    maxLength: 9,
    pattern: /^\d{9}$/,
    placeholder: '6 12 34 56 78',
    validate: (digits) => {
      return /^\d{9}$/.test(digits)
    }
  },
  {
    code: 'IT',
    name: '意大利',
    nameEn: 'Italy',
    dialCode: '+39',
    flag: 'IT',
    minLength: 9,
    maxLength: 10,
    pattern: /^\d{9,10}$/,
    placeholder: '312 345 6789',
    validate: (digits) => {
      return /^\d{9,10}$/.test(digits)
    }
  },
  {
    code: 'ES',
    name: '西班牙',
    nameEn: 'Spain',
    dialCode: '+34',
    flag: 'ES',
    minLength: 9,
    maxLength: 9,
    pattern: /^\d{9}$/,
    placeholder: '612 345 678',
    validate: (digits) => {
      return /^\d{9}$/.test(digits)
    }
  },
  {
    code: 'NL',
    name: '荷兰',
    nameEn: 'Netherlands',
    dialCode: '+31',
    flag: 'NL',
    minLength: 9,
    maxLength: 9,
    pattern: /^\d{9}$/,
    placeholder: '6 12345678',
    validate: (digits) => {
      return /^\d{9}$/.test(digits)
    }
  },
  {
    code: 'RU',
    name: '俄罗斯',
    nameEn: 'Russia',
    dialCode: '+7',
    flag: 'RU',
    minLength: 10,
    maxLength: 10,
    pattern: /^\d{10}$/,
    placeholder: '912 345 6789',
    validate: (digits) => {
      return /^\d{10}$/.test(digits)
    }
  },
  {
    code: 'BR',
    name: '巴西',
    nameEn: 'Brazil',
    dialCode: '+55',
    flag: 'BR',
    minLength: 10,
    maxLength: 11,
    pattern: /^\d{10,11}$/,
    placeholder: '11 91234 5678',
    validate: (digits) => {
      return /^\d{10,11}$/.test(digits)
    }
  },
  {
    code: 'MX',
    name: '墨西哥',
    nameEn: 'Mexico',
    dialCode: '+52',
    flag: 'MX',
    minLength: 10,
    maxLength: 10,
    pattern: /^\d{10}$/,
    placeholder: '55 1234 5678',
    validate: (digits) => {
      return /^\d{10}$/.test(digits)
    }
  },
  {
    code: 'ZA',
    name: '南非',
    nameEn: 'South Africa',
    dialCode: '+27',
    flag: 'ZA',
    minLength: 9,
    maxLength: 9,
    pattern: /^\d{9}$/,
    placeholder: '82 123 4567',
    validate: (digits) => {
      return /^\d{9}$/.test(digits)
    }
  },
  {
    code: 'EG',
    name: '埃及',
    nameEn: 'Egypt',
    dialCode: '+20',
    flag: 'EG',
    minLength: 10,
    maxLength: 10,
    pattern: /^\d{10}$/,
    placeholder: '100 123 4567',
    validate: (digits) => {
      return /^\d{10}$/.test(digits)
    }
  },
  {
    code: 'TR',
    name: '土耳其',
    nameEn: 'Turkey',
    dialCode: '+90',
    flag: 'TR',
    minLength: 10,
    maxLength: 10,
    pattern: /^\d{10}$/,
    placeholder: '532 123 4567',
    validate: (digits) => {
      return /^\d{10}$/.test(digits)
    }
  },
  {
    code: 'SA',
    name: '沙特阿拉伯',
    nameEn: 'Saudi Arabia',
    dialCode: '+966',
    flag: 'SA',
    minLength: 9,
    maxLength: 9,
    pattern: /^\d{9}$/,
    placeholder: '50 123 4567',
    validate: (digits) => {
      return /^\d{9}$/.test(digits)
    }
  },
  {
    code: 'AE',
    name: '阿联酋',
    nameEn: 'United Arab Emirates',
    dialCode: '+971',
    flag: 'AE',
    minLength: 9,
    maxLength: 9,
    pattern: /^\d{9}$/,
    placeholder: '50 123 4567',
    validate: (digits) => {
      return /^\d{9}$/.test(digits)
    }
  },
  {
    code: 'IL',
    name: '以色列',
    nameEn: 'Israel',
    dialCode: '+972',
    flag: 'IL',
    minLength: 9,
    maxLength: 9,
    pattern: /^\d{9}$/,
    placeholder: '50 123 4567',
    validate: (digits) => {
      return /^\d{9}$/.test(digits)
    }
  },
  {
    code: 'SE',
    name: '瑞典',
    nameEn: 'Sweden',
    dialCode: '+46',
    flag: 'SE',
    minLength: 7,
    maxLength: 9,
    pattern: /^\d{7,9}$/,
    placeholder: '70 123 45 67',
    validate: (digits) => {
      return /^\d{7,9}$/.test(digits)
    }
  },
  {
    code: 'NO',
    name: '挪威',
    nameEn: 'Norway',
    dialCode: '+47',
    flag: 'NO',
    minLength: 8,
    maxLength: 8,
    pattern: /^\d{8}$/,
    placeholder: '912 34 567',
    validate: (digits) => {
      return /^\d{8}$/.test(digits)
    }
  },
  {
    code: 'FI',
    name: '芬兰',
    nameEn: 'Finland',
    dialCode: '+358',
    flag: 'FI',
    minLength: 9,
    maxLength: 10,
    pattern: /^\d{9,10}$/,
    placeholder: '40 123 4567',
    validate: (digits) => {
      return /^\d{9,10}$/.test(digits)
    }
  },
  {
    code: 'DK',
    name: '丹麦',
    nameEn: 'Denmark',
    dialCode: '+45',
    flag: 'DK',
    minLength: 8,
    maxLength: 8,
    pattern: /^\d{8}$/,
    placeholder: '12 34 56 78',
    validate: (digits) => {
      return /^\d{8}$/.test(digits)
    }
  },
  {
    code: 'PL',
    name: '波兰',
    nameEn: 'Poland',
    dialCode: '+48',
    flag: 'PL',
    minLength: 9,
    maxLength: 9,
    pattern: /^\d{9}$/,
    placeholder: '123 456 789',
    validate: (digits) => {
      return /^\d{9}$/.test(digits)
    }
  },
  {
    code: 'UA',
    name: '乌克兰',
    nameEn: 'Ukraine',
    dialCode: '+380',
    flag: 'UA',
    minLength: 9,
    maxLength: 9,
    pattern: /^\d{9}$/,
    placeholder: '63 123 4567',
    validate: (digits) => {
      return /^\d{9}$/.test(digits)
    }
  },
  {
    code: 'CZ',
    name: '捷克',
    nameEn: 'Czech Republic',
    dialCode: '+420',
    flag: 'CZ',
    minLength: 9,
    maxLength: 9,
    pattern: /^\d{9}$/,
    placeholder: '123 456 789',
    validate: (digits) => {
      return /^\d{9}$/.test(digits)
    }
  },
  {
    code: 'HU',
    name: '匈牙利',
    nameEn: 'Hungary',
    dialCode: '+36',
    flag: 'HU',
    minLength: 9,
    maxLength: 9,
    pattern: /^\d{9}$/,
    placeholder: '30 123 4567',
    validate: (digits) => {
      return /^\d{9}$/.test(digits)
    }
  },
  {
    code: 'GR',
    name: '希腊',
    nameEn: 'Greece',
    dialCode: '+30',
    flag: 'GR',
    minLength: 10,
    maxLength: 10,
    pattern: /^\d{10}$/,
    placeholder: '691 234 5678',
    validate: (digits) => {
      return /^\d{10}$/.test(digits)
    }
  },
  {
    code: 'PT',
    name: '葡萄牙',
    nameEn: 'Portugal',
    dialCode: '+351',
    flag: 'PT',
    minLength: 9,
    maxLength: 9,
    pattern: /^\d{9}$/,
    placeholder: '912 345 678',
    validate: (digits) => {
      return /^\d{9}$/.test(digits)
    }
  },
  {
    code: 'AT',
    name: '奥地利',
    nameEn: 'Austria',
    dialCode: '+43',
    flag: 'AT',
    minLength: 10,
    maxLength: 11,
    pattern: /^\d{10,11}$/,
    placeholder: '664 123 45678',
    validate: (digits) => {
      return /^\d{10,11}$/.test(digits)
    }
  },
  {
    code: 'CH',
    name: '瑞士',
    nameEn: 'Switzerland',
    dialCode: '+41',
    flag: 'CH',
    minLength: 9,
    maxLength: 9,
    pattern: /^\d{9}$/,
    placeholder: '79 123 45 67',
    validate: (digits) => {
      return /^\d{9}$/.test(digits)
    }
  },
  {
    code: 'BE',
    name: '比利时',
    nameEn: 'Belgium',
    dialCode: '+32',
    flag: 'BE',
    minLength: 9,
    maxLength: 9,
    pattern: /^\d{9}$/,
    placeholder: '471 12 34 56',
    validate: (digits) => {
      return /^\d{9}$/.test(digits)
    }
  },
  {
    code: 'IE',
    name: '爱尔兰',
    nameEn: 'Ireland',
    dialCode: '+353',
    flag: 'IE',
    minLength: 9,
    maxLength: 9,
    pattern: /^\d{9}$/,
    placeholder: '87 123 4567',
    validate: (digits) => {
      return /^\d{9}$/.test(digits)
    }
  },
  {
    code: 'NZ',
    name: '新西兰',
    nameEn: 'New Zealand',
    dialCode: '+64',
    flag: 'NZ',
    minLength: 9,
    maxLength: 10,
    pattern: /^\d{9,10}$/,
    placeholder: '21 123 4567',
    validate: (digits) => {
      return /^\d{9,10}$/.test(digits)
    }
  },
  {
    code: 'PK',
    name: '巴基斯坦',
    nameEn: 'Pakistan',
    dialCode: '+92',
    flag: 'PK',
    minLength: 10,
    maxLength: 10,
    pattern: /^\d{10}$/,
    placeholder: '300 1234567',
    validate: (digits) => {
      return /^\d{10}$/.test(digits)
    }
  },
  {
    code: 'BD',
    name: '孟加拉国',
    nameEn: 'Bangladesh',
    dialCode: '+880',
    flag: 'BD',
    minLength: 10,
    maxLength: 10,
    pattern: /^\d{10}$/,
    placeholder: '171 1234567',
    validate: (digits) => {
      return /^\d{10}$/.test(digits)
    }
  },
  {
    code: 'NG',
    name: '尼日利亚',
    nameEn: 'Nigeria',
    dialCode: '+234',
    flag: 'NG',
    minLength: 10,
    maxLength: 10,
    pattern: /^\d{10}$/,
    placeholder: '801 234 5678',
    validate: (digits) => {
      return /^\d{10}$/.test(digits)
    }
  },
  {
    code: 'KE',
    name: '肯尼亚',
    nameEn: 'Kenya',
    dialCode: '+254',
    flag: 'KE',
    minLength: 9,
    maxLength: 9,
    pattern: /^\d{9}$/,
    placeholder: '712 345 678',
    validate: (digits) => {
      return /^\d{9}$/.test(digits)
    }
  },
  {
    code: 'AR',
    name: '阿根廷',
    nameEn: 'Argentina',
    dialCode: '+54',
    flag: 'AR',
    minLength: 10,
    maxLength: 10,
    pattern: /^\d{10}$/,
    placeholder: '11 1234 5678',
    validate: (digits) => {
      return /^\d{10}$/.test(digits)
    }
  },
  {
    code: 'CL',
    name: '智利',
    nameEn: 'Chile',
    dialCode: '+56',
    flag: 'CL',
    minLength: 9,
    maxLength: 9,
    pattern: /^\d{9}$/,
    placeholder: '9 1234 5678',
    validate: (digits) => {
      return /^\d{9}$/.test(digits)
    }
  },
  {
    code: 'CO',
    name: '哥伦比亚',
    nameEn: 'Colombia',
    dialCode: '+57',
    flag: 'CO',
    minLength: 10,
    maxLength: 10,
    pattern: /^\d{10}$/,
    placeholder: '300 123 4567',
    validate: (digits) => {
      return /^\d{10}$/.test(digits)
    }
  },
  {
    code: 'PE',
    name: '秘鲁',
    nameEn: 'Peru',
    dialCode: '+51',
    flag: 'PE',
    minLength: 9,
    maxLength: 9,
    pattern: /^\d{9}$/,
    placeholder: '912 345 678',
    validate: (digits) => {
      return /^\d{9}$/.test(digits)
    }
  }
]

/**
 * 根据国家代码获取区号信息
 * @param {string} countryCode - 国家代码，如 'CN'
 * @returns {Object|undefined}
 */
export function getCountryByCode(countryCode) {
  return countryCodes.find(c => c.code === countryCode.toUpperCase())
}

/**
 * 根据区号获取国家信息
 * @param {string} dialCode - 区号，如 '+86'
 * @returns {Object|undefined}
 */
export function getCountryByDialCode(dialCode) {
  return countryCodes.find(c => c.dialCode === dialCode)
}

/**
 * 智能检测默认国家
 * 优先根据浏览器语言设置， fallback 到中国
 * @returns {string} 国家代码
 */
export function detectDefaultCountry() {
  try {
    const lang = navigator.language || navigator.userLanguage || 'zh-CN'
    const langMap = {
      'zh': 'CN',
      'zh-CN': 'CN',
      'zh-TW': 'TW',
      'zh-HK': 'HK',
      'en': 'US',
      'en-US': 'US',
      'en-GB': 'GB',
      'ja': 'JP',
      'ko': 'KR',
      'fr': 'FR',
      'de': 'DE',
      'es': 'ES',
      'it': 'IT',
      'ru': 'RU',
      'pt': 'PT',
      'ar': 'SA',
      'hi': 'IN',
      'th': 'TH',
      'vi': 'VN',
      'ms': 'MY',
      'id': 'ID',
      'tl': 'PH'
    }
    return langMap[lang] || 'CN'
  } catch {
    return 'CN'
  }
}
