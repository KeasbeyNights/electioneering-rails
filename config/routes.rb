ElectioneeringRails::Application.routes.draw do
  match "compare" => "home#compare"

  namespace :api, defaults: {format: 'json'} do
    namespace :v1 do
      resources :politicians
    end
  end

  root :to => 'home#index'
end
