import React from 'react';
import { GoogleOAuthProvider, GoogleLogin } from '@react-oauth/google';
import { useAuth } from '../contexts/AuthContext';
import { MapPin, Calendar, Users, Star, ArrowRight, Sparkles, Globe, Shield } from 'lucide-react';
import { supabase } from '../supabaseClient';

const LandingPage = ({ onNavigate }) => {
  const { login } = useAuth();

  const handleGoogleSuccess = async (response) => {
    const payload = JSON.parse(atob(response.credential.split('.')[1]));
    const userData = {
      email: payload.email,
      google_id: payload.sub, // Store Google ID in a separate column
    };

    try {
      const { error } = await supabase
        .from('users')
        .upsert([userData], { onConflict: ['email'] });

      if (error) throw error;

      login(userData);
      if (onNavigate) onNavigate('dashboard');
    } catch (error) {
      console.error('Failed to store user in Supabase:', error);
    }
  };

  const handleGoogleError = () => {
    console.error('Google login failed');
  };

  return (
    <GoogleOAuthProvider clientId={import.meta.env.VITE_GOOGLE_CLIENT_ID || "your-google-client-id"}>
      <div className="min-h-screen bg-gray-900 text-white">
        {/* Header */}
        <header className="relative z-50 px-6 py-6">
          <div className="max-w-7xl mx-auto flex justify-between items-center">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl">
                <MapPin className="h-6 w-6 text-white" />
              </div>
              <span className="text-2xl  font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                AI itineraries
              </span>
            </div>
            <nav className="hidden md:flex space-x-8">
              <a href="" className="text-gray-300 hover:text-white transition-colors">Features</a>
              <a href="" className="text-gray-300 hover:text-white transition-colors">Reviews</a>
              <a href="" className="text-gray-300 hover:text-white transition-colors">Pricing</a>
            </nav>
          </div>
        </header>

        {/* Hero Section */}
        <main className="relative">
          {/* Background Elements */}
          <div className="absolute inset-0 overflow-hidden">
            <div className="absolute -top-40 -right-40 w-80 h-80 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse"></div>
            <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-blue-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse"></div>
          </div>

          <div className="relative max-w-7xl mx-auto px-6 py-20">
            {/* Hero Content */}
            <div className="text-center max-w-4xl mx-auto mb-20">
              <div className="flex justify-center mb-6">
                <div className="flex items-center space-x-2 bg-gray-800 px-4 py-2 rounded-full border border-gray-700">
                  <Sparkles className="h-4 w-4 text-yellow-400" />
                  <span className="text-sm text-gray-300">AI-Powered Travel Planning</span>
                </div>
              </div>

              <h1 className="text-5xl md:text-7xl font-bold mb-8 leading-tight">
                Plan Your Perfect
                <span className="block bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
                  Adventure
                </span>
              </h1>

              <p className="text-xl md:text-2xl text-gray-300 mb-12 leading-relaxed max-w-3xl mx-auto">
                Create intelligent travel itineraries, discover hidden gems, and make unforgettable memories with our AI-powered planning platform.
              </p>

            
              <div className="bg-gray-800 p-8 rounded-2xl border border-gray-700 max-w-md mx-auto backdrop-blur-sm">
                <h2 className="text-2xl font-bold mb-2">Start Planning Today</h2>
                <p className="text-gray-400 mb-6">Join thousands of travelers who trust TravelPlan</p>
                
                <div className="space-y-4 gap-x-1.5">
                  <GoogleLogin
                    onSuccess={handleGoogleSuccess}
                    onError={handleGoogleError}
                    theme="filled_black"
                    size="medium"
                    width="6969"
                    shape="pill"
                  />
                  <p className="text-xs text-gray-500">
                    Free to start • No credit card required
                  </p>
                </div>
              </div>
            </div>

            {/* Features Grid */}
            <div id="features" className="grid md:grid-cols-3 gap-8 mb-20">
              <div className="group p-8 bg-gray-800 rounded-2xl border border-gray-700 hover:border-blue-500 transition-all duration-300 hover:transform hover:scale-105">
                <div className="flex items-center justify-center w-14 h-14 bg-gradient-to-r from-blue-500 to-blue-600 rounded-xl mb-6 group-hover:from-blue-400 group-hover:to-blue-500 transition-all">
                  <Calendar className="h-7 w-7 text-white" />
                </div>
                <h3 className="text-xl font-bold mb-4">Smart Planning</h3>
                <p className="text-gray-400 leading-relaxed">
                  AI-powered itinerary creation that adapts to your preferences, budget, and travel style for the perfect trip.
                </p>
              </div>

              <div className="group p-8 bg-gray-800 rounded-2xl border border-gray-700 hover:border-purple-500 transition-all duration-300 hover:transform hover:scale-105">
                <div className="flex items-center justify-center w-14 h-14 bg-gradient-to-r from-purple-500 to-purple-600 rounded-xl mb-6 group-hover:from-purple-400 group-hover:to-purple-500 transition-all">
                  <Globe className="h-7 w-7 text-white" />
                </div>
                <h3 className="text-xl font-bold mb-4">Discover Places</h3>
                <p className="text-gray-400 leading-relaxed">
                  Explore hidden gems and popular attractions with insider tips and local recommendations.
                </p>
              </div>

              <div className="group p-8 bg-gray-800 rounded-2xl border border-gray-700 hover:border-green-500 transition-all duration-300 hover:transform hover:scale-105">
                <div className="flex items-center justify-center w-14 h-14 bg-gradient-to-r from-green-500 to-green-600 rounded-xl mb-6 group-hover:from-green-400 group-hover:to-green-500 transition-all">
                  <Shield className="h-7 w-7 text-white" />
                </div>
                <h3 className="text-xl font-bold mb-4">Secure & Reliable</h3>
                <p className="text-gray-400 leading-relaxed">
                  Your data is protected with enterprise-grade security. Plan with confidence and peace of mind.
                </p>
              </div>
            </div>

            {/* Stats Section */}
            <div className="bg-gradient-to-r from-gray-800 to-gray-900 rounded-2xl p-8 border border-gray-700 mb-20">
              <div className="grid md:grid-cols-4 gap-8 text-center">
                <div>
                  <div className="text-3xl font-bold text-blue-400 mb-2">200</div>
                  <div className="text-gray-400">Happy Travelers</div>
                </div>
                <div>
                  <div className="text-3xl font-bold text-purple-400 mb-2">120+</div>
                  <div className="text-gray-400">Destinations</div>
                </div>
                <div>
                  <div className="text-3xl font-bold text-green-400 mb-2">95%</div>
                  <div className="text-gray-400">Satisfaction Rate</div>
                </div>
                <div>
                  <div className="text-3xl font-bold text-yellow-400 mb-2">24/7</div>
                  <div className="text-gray-400">Support</div>
                </div>
              </div>
            </div>


            {/* CTA Section */}
            <div className="text-center bg-gradient-to-r from-blue-600 to-purple-600 p-12 rounded-2xl">
              <h2 className="text-4xl font-bold mb-4">Ready to Start Your Journey?</h2>
              <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
                Join thousands of travelers who have discovered their perfect trips with TravelPlan
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
                <div className="bg-white p-4 rounded-xl">
                  <GoogleLogin
                    onSuccess={handleGoogleSuccess}
                    onError={handleGoogleError}
                    theme="outline"
                    size="large"
                  />
                </div>
                <div className="flex items-center text-blue-100">
                  <ArrowRight className="h-5 w-5 mr-2" />
                  <span>Get started in 30 seconds</span>
                </div>
              </div>
            </div>
          </div>
        </main>

        {/* Footer */}
        <footer className="bg-gray-950 border-t border-gray-800 py-12 px-6 mt-20">
          <div className="max-w-7xl mx-auto">
            <div className="grid md:grid-cols-4 gap-8 mb-8">
              <div>
                <div className="flex items-center space-x-3 mb-4">
                  <div className="p-2 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl">
                    <MapPin className="h-5 w-5 text-white" />
                  </div>
                  <span className="text-xl font-bold">TravelPlan</span>
                </div>
                <p className="text-gray-400 leading-relaxed">
                  Making travel planning simple, intelligent, and enjoyable for everyone.
                </p>
              </div>
              
              <div>
                <h4 className="text-white font-semibold mb-4">Product</h4>
                <ul className="space-y-2 text-gray-400">
                  <li><a href="#" className="hover:text-white transition-colors">Features</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">Pricing</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">API</a></li>
                </ul>
              </div>
              
              <div>
                <h4 className="text-white font-semibold mb-4">Company</h4>
                <ul className="space-y-2 text-gray-400">
                  <li><a href="#" className="hover:text-white transition-colors">About</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">Blog</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">Careers</a></li>
                </ul>
              </div>
              
              <div>
                <h4 className="text-white font-semibold mb-4">Support</h4>
                <ul className="space-y-2 text-gray-400">
                  <li><a href="#" className="hover:text-white transition-colors">Help Center</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">Contact</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">Privacy</a></li>
                </ul>
              </div>
            </div>
            
          
          </div>
        </footer>
      </div>
    </GoogleOAuthProvider>
  );
};

export default LandingPage;