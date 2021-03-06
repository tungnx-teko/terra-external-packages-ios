Pod::Spec.new do |s|
	s.name                   = 'CallAppSDK'
	s.version                = '0.0.1'
	s.summary                = 'CallAppSDK.framework'
	s.homepage               = 'https://github.com/teko-vn/Specs-ios.git'
	s.license                = { :type => 'MIT', :file => 'LICENSE' }

	s.source                 = { :http => 'https://github.com/tungnx-teko/terra-external-packages-ios/releases/download/2020.10.26T04.41.54/CallAppSDK.framework.zip' }
	s.vendored_frameworks    = 'CallAppSDK.framework'
	s.public_header_files    = 'CallAppSDK.framework/Headers/*.h'
	s.source_files           = 'CallAppSDK.framework/Headers/*.{h,m,swift}'

	s.author                 = {'Mobile Lab' => 'mobile.lab@teko.vn'}

	s.dependency 'Alamofire', '~> 4.8.2'
	s.dependency 'Kingfisher'
end