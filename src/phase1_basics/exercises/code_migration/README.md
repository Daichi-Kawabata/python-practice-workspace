# コード移植課題

## Ruby → Python 移植

### 元のRubyコード (参考)
```ruby
require 'net/http'
require 'json'

class ApiClient
  def initialize(base_url)
    @base_url = base_url
  end
  
  def fetch_users
    uri = URI("#{@base_url}/users")
    response = Net::HTTP.get_response(uri)
    
    case response.code
    when '200'
      JSON.parse(response.body)
    when '404'
      raise "Users not found"
    else
      raise "API Error: #{response.code}"
    end
  rescue => e
    puts "Error: #{e.message}"
    []
  end
end
```
